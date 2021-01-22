from random import choice
from string import ascii_letters
from tabulate import tabulate


def create_devices(num_devices=1, num_subnets=1):
    created_device = []

    if num_devices > 254 or num_subnets > 254:
        print("Error: too many devices and/or subnets requested")
        return created_device
    for subnet_index in range(1, num_subnets + 1):

        for devices_index in range(1, num_devices + 1):

            device = {}
            device["name"] = f'{choice(["r2", "r3", "r4", "r6", "r10"])}-' \
                             f'{choice(["L", "U"])}' \
                             f'{choice(ascii_letters)}'
            device["vendor"] = choice(["cisco", "juniper", "arista"])
            if device["vendor"] == "cisco":
                device["os"] = choice(["ios", "iosxe", "iosxr", "nexus"])
                if device["os"] == "ios":
                    device["version"] = choice(["15", "15E", "15SY", "12.2SE"])
                elif device["os"] == "iosxe":
                    device["version"] = choice(["16.9", "16.7", "16.5", "16.3"])
                elif device["os"] == "iosxr":
                    device["version"] = choice(["6.2", "6.0", "5.4", "5.1"])
                elif device["os"] == "nexus":
                    device["version"] = choice(["8.2", "8.0", "7.3", "7.1"])
            elif device["vendor"] == "juniper":
                device["os"] = "junos"
                device["version"] = choice(["12.3R12-S15", "15.1R7-S6", "18.4R2-S3", "15.1X53-D591"])
            elif device["vendor"] == "arista":
                device["os"] = "eos"
                device["version"] = choice(["4.24.1F", "4.23.2F", "4.22.1F", "4.21.3F"])
            device['ip'] = f"10.0.{subnet_index}.{devices_index}"

            created_device.append(device)

    return created_device


if __name__ == "__main__":
    devices = create_devices(num_devices=5, num_subnets=4)
    print(f'{tabulate(devices, headers="keys"):>16}')
