import re
from netmiko import Netmiko
import napalm
import urllib3
from ncclient import manager
import xmltodict
from pprint import pprint
from rich import print

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DeviceType:
    IOS = "ios"
    NXOS = "nxos"
    NXOS_SSH = "nxos_ssh"
    NEXUS = "nexus"
    CISCO_NXOS = "cisco_nxos"
    JUNOS = "junos"
    JUNIPER = "juniper"


class Device:

    def __init__(self, name, device_type, hostname):
        self.name = name
        self.device_type = device_type
        self.hostname = hostname

        self.mac = None
        self.ip = None
        self.connection = None

        self.username = None
        self.password = None
        self.port = None

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def set_port(self, port):
        self.port = port

    def connect(self):
        raise NotImplementedError("Please implement the connect() method")

    def get_facts(self):
        raise NotImplementedError("Please implement the get_facts() method")

    def disconnect(self):
        raise NotImplementedError("Please implement the disconnect() method")


def get_version_from_show(show_version_output):
    re_nxos_version_pattern = r"NXOS: version (.*)"
    nxos_version_match = re.search(re_nxos_version_pattern, show_version_output)

    if nxos_version_match:
        return nxos_version_match.group(1)
    else:
        return None


def get_uptime_from_show(show_uptime_output):
    uptime_lines = show_uptime_output.splitlines()
    for line in uptime_lines:
        if "System uptime:" in line:
            uptime_parts = line.split()
            days = int(uptime_parts[2])
            hours = int(uptime_parts[4])
            minutes = int(uptime_parts[6])
            seconds = int(uptime_parts[8])
            return days * 86400 + hours * 3600 + minutes * 60 + seconds


def junos_get_information(show_hostname_output):
    information = {}
    pattern = re.compile(r"Model: (.*)")
    model = pattern.search(show_hostname_output)
    if model:
        information['model'] = model.group(1)
    else:
        information['model'] = None
    pattern = re.compile(r"Junos: (.*)")
    model = pattern.search(show_hostname_output)
    if model:
        information['Version'] = model.group(1)
    else:
        information['Version'] = None

    pattern = re.compile(r"Hostname: (.*)")
    model = pattern.search(show_hostname_output)
    if model:
        information['Hostname'] = model.group(1)
    else:
        information['Hostname'] = None

    pattern = re.compile(r"Family: (.*)")
    model = pattern.search(show_hostname_output)
    if model:
        information['Family'] = model.group(1)
    else:
        information['Family'] = None

    return information


def junos_get_uptime_from_show(show_uptime_output):
    re_junos_uptime = re.compile(r'System booted: .*\((\d{2}:\d{2}:\d{2}) ago\)')
    junos_uptime_match = re_junos_uptime.search(show_uptime_output)
    if junos_uptime_match:
        uptime = junos_uptime_match.group(1)
        uptime_split = uptime.split(":")

        hours = int(uptime_split[0])
        minutes = int(uptime_split[1])
        seconds = int(uptime_split[2])
        return hours * 3600 + minutes * 60 + seconds


def junos_get_serial_number(show_serial_output):
    re_serial_number = re.compile(r"Chassis\s*(\w*)\s*")
    serial_number_match = re_serial_number.search(show_serial_output)
    if serial_number_match:
        return serial_number_match.group(1)


class NetmikoDevice(Device):

    def connect(self):
        print(f"\n\n----- Connecting to {self.hostname}:{self.port}")
        self.connection = Netmiko(
            self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            device_type=self.device_type,
        )

        print(f"----- Connected! --------------------")
        return True

    def get_facts(self):

        facts = dict()

        if self.device_type == DeviceType.CISCO_NXOS:
            show_hostname_output = self.connection.send_command("show hostname")
            show_version_output = self.connection.send_command("show version")
            show_serial_output = self.connection.send_command("show license host-id")
            show_uptime_output = self.connection.send_command("show system uptime")

            facts["os_version"] = get_version_from_show(show_version_output)
            facts["hostname"] = show_hostname_output.strip()
            facts["serial_number"] = show_serial_output.strip()[20:]  # Don't do this :-)
            facts["uptime"] = get_uptime_from_show(show_uptime_output)


        elif self.device_type == DeviceType.JUNIPER:
            show_hostname_output = self.connection.send_command("show system information")
            show_uptime_output = self.connection.send_command("show system uptime")
            show_serial_output = self.connection.send_command("show chassis hardware")

            information = junos_get_information(show_hostname_output)
            facts["os_version"] = information['Version']
            facts["model"] = information['model']
            facts["Hostname"] = information['Hostname']
            facts["Family"] = information['Family']
            facts["serial_number"] = junos_get_serial_number(show_serial_output)
            facts["uptime"] = junos_get_uptime_from_show(show_uptime_output)
            facts['vendor'] = 'Juniper'

        else:
            return False
        return facts

    def disconnect(self):
        self.connection.disconnect()
        print(f"----- Disconnected! --------------------")
        return True


class NapalmDevice(Device):

    def connect(self):
        driver = napalm.get_network_driver(self.device_type)
        if self.device_type == DeviceType.NXOS:
            self.connection = driver(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
            )

        elif self.device_type == DeviceType.JUNOS:
            self.connection = driver(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
            )

        elif self.device_type == DeviceType.IOS or self.device_type == DeviceType.NXOS_SSH:
            self.connection = driver(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                optional_args={"port": self.port},
            )
        else:
            return False

        print(f"\n\n----- Connecting to {self.hostname}:{self.port}")
        self.connection.open()
        print(f"----- Connected! --------------------")

        return True

    def get_facts(self):
        return self.connection.get_facts()

    def disconnect(self):
        self.connection.close()
        print(f"----- Disconnected! --------------------")
        return True


class NcclientDevice(Device):

    def connect(self):
        print(f"\n\n----- Connecting to {self.hostname}:{self.port}")
        self.connection = manager.connect(
            host=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            device_params={"name": self.device_type},
            hostkey_verify=False,
        )
        print(f"----- Connected! --------------------")

        return True

    def get_facts(self):
        facts = dict()

        serial_number_xml_nxos = '<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><serial/></System>'
        rsp = self.connection.get(("subtree", serial_number_xml_nxos))
        serial_xml = xmltodict.parse(rsp.data_xml, dict_constructor=dict)

        facts["serial_number"] = serial_xml["data"]["System"]["serial"]

        return facts

    def disconnect(self):
        self.connection.close_session()
        print(f"----- Disconnected! --------------------")
        return True


def create_devices():
    created_devices = dict()
    created_devices["nxos-netmiko"] = NetmikoDevice(
        name="nxos-netmiko",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.CISCO_NXOS
    )
    created_devices["nxos-netmiko"].set_port(8181)
    created_devices["nxos-netmiko"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["nxos-napalm"] = NapalmDevice(
        name="nxos-napalm",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.NXOS,
    )
    created_devices["nxos-napalm"].set_port(8181)
    created_devices["nxos-napalm"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["nxos-ncclient"] = NcclientDevice(
        name="nxos-ncclient",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.NEXUS,
    )
    created_devices["nxos-ncclient"].set_port(10000)
    created_devices["nxos-ncclient"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["junos-napalm"] = NapalmDevice(
        name="junos-napalm",
        hostname="192.168.1.213",
        device_type=DeviceType.JUNOS,
    )
    created_devices["junos-napalm"].set_credentials(username="admin", password="juniper1")

    created_devices["junos-netmiko"] = NetmikoDevice(
        name="junos-netmiko",
        hostname="192.168.1.213",
        device_type=DeviceType.JUNIPER
    )
    created_devices["junos-netmiko"].set_credentials(username="admin", password="juniper1")

    created_devices["junos-srx-napalm"] = NapalmDevice(
        name="junos-srx-napalm",
        hostname="192.168.1.229",
        device_type=DeviceType.JUNOS,
    )
    created_devices["junos-srx-napalm"].set_credentials(username="admin", password="juniper1")

    created_devices["junos-srx-netmiko"] = NetmikoDevice(
        name="junos-srx-netmiko",
        hostname="192.168.1.229",
        device_type=DeviceType.JUNIPER
    )
    created_devices["junos-srx-netmiko"].set_credentials(username="admin", password="juniper1")

    return created_devices


devices = create_devices()
for _, device in devices.items():

    if not device.connect():
        print(f"----- Connection failed: {device.name}")
        continue

    facts = device.get_facts()
    print(f"----- Facts for device: {device.name}")
    pprint(facts)
    device.disconnect()
