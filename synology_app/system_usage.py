from synology_dsm import SynologyDSM
from pprint import pprint

print("Creating Valid API")
api = SynologyDSM("192.168.1.12", "5000", "aramide", "olfAS1q8ma8N")
system = api.system

system.update()

# Get CPU information

print("=====Get CPU information=====")
print(system.cpu_clock_speed)
print(system.cpu_cores)
print(system.cpu_family)
print(system.cpu_series)

# Get NTP settings
print("======Get NTP settings=====")
print(system.enabled_ntp)
print(system.ntp_server)

# Get system information
print("======Get system information=====")
print(system.firmware_ver)
print(system.model)
print(system.ram_size)
print(system.serial)
print(system.sys_temp)
print(system.time)
print(system.time_zone)
print(system.time_zone_desc)
print(system.up_time)

# Get list of all connected USB devices
print("======Get list of all connected USB devices=====")
pprint(system.usb_dev)