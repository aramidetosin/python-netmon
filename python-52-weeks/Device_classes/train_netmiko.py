import re
from netmiko import Netmiko

junos = {
    "hostname": "192.168.1.229",
    "username": "admin",
    "password": "juniper1",
    "device_type": "juniper",
}

connection = Netmiko(
    host=junos["hostname"],
    username=junos["username"],
    password=junos["password"],
    device_type=junos["device_type"],
)

show_hostname_output = connection.send_command("show system information")
show_uptime_output = connection.send_command("show system uptime")
show_serial_output = connection.send_command("show chassis hardware")
show_interface_output = connection.send_command("show interface terse")
print(show_hostname_output)
print(show_uptime_output)
print(show_serial_output)
print(show_interface_output)


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


print(junos_get_information(show_hostname_output))

print(junos_get_uptime_from_show(show_uptime_output))

print(junos_get_serial_number(show_serial_output))


line_show_interface_output = show_interface_output.splitlines()
interfaces = []
for line in line_show_interface_output:
    xx = line.split(" ")[0]
    if xx != "Interface" and xx != '':
        if '.' not in xx:
            interfaces.append(xx)

print(interfaces)
