from l_03_functions import create_devices
from tabulate import tabulate
from pprint import pprint
from operator import itemgetter

devices = create_devices(num_devices=5, num_subnets=4)

print(f'{tabulate(devices, headers="keys"):>16}')

print("\n\nUSING PRINT")
print(devices)

print("\n\nUSING PPRINT")
pprint(devices)

from time import sleep
from datetime import datetime

for device in devices:
    sleep(0.1)
    device["last_heard"] = str(datetime.now())
    print(device)

print("\n\nUSING TABULATE")
print(tabulate(sorted(devices, key=itemgetter("vendor", "os", "version")), headers='keys'))

print("\n\nUSING LOOP AND F-STRING")
print("   NAME      VENDOR : OS      IP ADDRESS       LAST HEARD")
print("  -----     -------   -----   --------------   ----------------------")
for device in devices:
    print(
        f'{device["name"]:7}  {device["vendor"]:>10} : {device["os"]:<6}  {device["ip"]:<15}  {device["last_heard"][:-4]}')

print("\nSame thing, but sorted descending by last_heard")
for device in sorted(devices, key=itemgetter("last_heard"), reverse=True):
    print(
        f'{device["name"]:7}  {device["vendor"]:>10} : {device["os"]:<6}  {device["ip"]:<15}  {device["last_heard"][:-4]}')

from random import choice

print("\n\nMULTIPLE PRINT STATEMENTS, SAME LINE")
print("Testing Devices:")
for device in devices:
    print(f"--- testing device {device['name']} ... ", end="")
    sleep(choice([0.1, 0.2, 0.3, 0.4]))
    print("done.")

print("Testing completed")

from rich import print
ip="192.168.1.14"
import nmap3
nmap = nmap3.Nmap()
results = nmap.nmap_os_detection(ip)
print(results)
# while True:
#
#     ip = input("\nInput IP address to scan: ")
#     if not ip:
#         break
#
#     print(f"\n--- beginning scan of {ip}")
#     output = nm.scan_top_ports(ip)
#     # print(f"------- command: {nm.command_line()}")
#
#     print("----- nmap scan output -------------------")
#     pprint(output)