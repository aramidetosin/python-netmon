from random import choice
from string import ascii_letters
from pprint import pprint
from tabulate import tabulate
from operator import itemgetter

devices = []
for index in range(1, 10):
    device = {}

    device["name"] = f'{choice(["r2", "r3", "r4", "r6", "r10"])}-' \
                     f'{choice(["L", "U"])}' \
                     f'{choice(ascii_letters)}'
    device['vendor'] = f'{choice(["cisco", "juniper", "arista"])}'
    if device['vendor'] == 'cisco':
        device["os"] = choice(["ios", "iosxe", "iosxr", "nexus"])
        device["version"] = choice(["12.1(T).04", "14.07X", "8.12(S).010", "20.45"])
    elif device["vendor"] == "juniper":
        device["os"] = "junos"
        device["version"] = choice(["J6.23.1", "8.43.12", "6.45", "6.03"])
    elif device["vendor"] == "arista":
        device["os"] = "eos"
        device["version"] = choice(["2.45", "2.55", "2.92.145", "3.01"])

    device['ip'] = f'10.0.0.{index}'

    for key, value in device.items():
        print(f'{key:>16} : {value}')

    devices.append(device)
print("\n----- DEViCES AS LIST OF DICTS --------------------")
pprint(devices)

print("\n----- SORTED DEVICES IN TABULAR FORMAT --------------------")
sorted_device = sorted(devices, key=itemgetter("vendor", "os", "version"))
print(tabulate(sorted_device, headers="keys"))
