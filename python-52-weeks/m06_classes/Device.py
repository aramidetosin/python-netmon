from netmiko import Netmiko
import napalm
from ncclient import manager
import re
import xmltodict
from pprint import pprint
import urllib3

class TransportType:
    NAPALM = "napalm"
    NCCLIENT = "ncclient"
    NETMIKO = "netmiko"


class DeviceType:
    IOS = "ios"
    NXOS = "nxos"
    NXOS_SSH = "nxos_ssh"
    NEXUS = "nexus"
    CISCO_NXOS = "cisco_nxos"

# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def connect_netmiko(hostname, username, password, port, device_type):
    print(f"\n\n----- Connecting to {hostname}:{port}")
    netmiko_connection = Netmiko(
        hostname,
        port=port,
        username=username,
        password=password,
        device_type=device_type,
    )
    print(f"----- Connected! --------------------")
    return netmiko_connection

def disconnect_netmiko(connection):
    connection.disconnect()
    print(f"----- Disconnected! --------------------")

def connect_napalm(hostname, username, password, port, device_type):
    driver = napalm.get_network_driver(device_type)
    if device_type == DeviceType.NXOS:
        napalm_device = driver(
            hostname=hostname,
            username=username,
            password=password,
        )
    elif device_type == DeviceType.IOS or device_type == DeviceType.NXOS_SSH:
        napalm_device = driver(
            hostname=hostname,
            username=username,
            password=password,
             optional_args={"port": port},
        )
    else:
        return None
    
    print(f"\n\n----- Connecting to {hostname}:{port}")
    napalm_device.open()
    print(f"----- Connected! --------------------")
    return napalm_device

def disconnect_napalm(connection):
    connection.close()
    print(f"----- Disconnected! --------------------")

def connect_ncclient(hostname, username, password, port,device_type):
    print(f"\n\n----- Connecting to {hostname}:{port}")
    nc_connection = manager.connect(
        host=hostname,
        port=port,
        username=username,
        password=password,
        device_params={"name": device_type},
        hostkey_verify=False,
    )
    print(f"----- Connected! --------------------")

    return nc_connection


def disconnect_ncclient(connection):
    connection.close_session()
    print(f"----- Disconnected! --------------------")

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
            return days*86400 + hours*3600 + minutes*60 + seconds


def get_facts_netmiko(connection):

    show_hostname_output = connection.send_command("show hostname")
    show_version_output = connection.send_command("show version")
    show_serial_output = connection.send_command("show license host-id")
    show_uptime_output = connection.send_command("show system uptime")

    facts = dict()
    facts["os_version"] = get_version_from_show(show_version_output)
    facts["hostname"] = show_hostname_output.strip()
    facts["serial_number"] = show_serial_output.strip()[20:]  # Don't do this :-)
    facts["uptime"] = get_uptime_from_show(show_uptime_output)

    return facts


def get_facts_napalm(connection):

    return connection.get_facts()


def get_facts_ncclient(connection):

    facts = dict()

    serial_number_xml_nxos = '<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><serial/></System>'
    rsp = connection.get(("subtree", serial_number_xml_nxos))
    serial_xml = xmltodict.parse(rsp.data_xml, dict_constructor=dict)

    facts["serial_number"] = serial_xml["data"]["System"]["serial"]

    return facts

class Device:
    def __init__ (self, name, device_type, hostname, transport):
        self.name = name
        self.device_type = device_type
        self.hostname = hostname
        self.transport = transport

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

        if self.transport == TransportType.NAPALM:
            self.connection = connect_napalm(
                self.hostname, self.username, self.password, self.port, self.device_type
            )
        elif self.transport == TransportType.NCCLIENT:
            self.connection = connect_ncclient(
                self.hostname, self.username, self.password, self.port, self.device_type
            )
        elif self.transport == TransportType.NETMIKO:
            self.connection = connect_netmiko(
                self.hostname, self.username, self.password, self.port, self.device_type
            )

        return True
    
    def get_facts(self):

        if self.transport == TransportType.NAPALM:
            return get_facts_napalm(self.connection)
        elif self.transport == TransportType.NCCLIENT:
            return get_facts_ncclient(self.connection)
        elif self.transport == TransportType.NETMIKO:
            return get_facts_netmiko(self.connection)

        return None

    def disconnect(self):

        if self.transport == TransportType.NAPALM:
            disconnect_napalm(self.connection)
        elif self.transport == TransportType.NCCLIENT:
            disconnect_ncclient(self.connection)
        elif self.transport == TransportType.NETMIKO:
            disconnect_netmiko(self.connection)

        return

def create_devices():
    created_devices = dict()
    created_devices["nxos-netmiko"] = Device(
        name="nxos-netmiko",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.CISCO_NXOS,
        transport=TransportType.NETMIKO,
    )
    created_devices["nxos-netmiko"].set_port(8181)
    created_devices["nxos-netmiko"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["nxos-napalm"] = Device(
        name="nxos-napalm",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.NXOS,
        transport=TransportType.NAPALM,
    )
    created_devices["nxos-napalm"].set_port(8181)
    created_devices["nxos-napalm"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["nxos-ncclient"] = Device(
        name="nxos-ncclient",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.NEXUS,
        transport=TransportType.NCCLIENT,
    )
    created_devices["nxos-ncclient"].set_port(10000)
    created_devices["nxos-ncclient"].set_credentials(username="admin", password="Admin_1234!")

    return created_devices

devices = create_devices()
for _, device in devices.items():
    if device.connect():
        facts = device.get_facts()
        print(f"----- Facts for device: {device.name}")
        pprint(facts)
    else:
        print(f"----- Connection failed: {device.name}")
        continue
    
    device.disconnect()
