from pprint import pprint as pp

# DICTIONARY representing a device
device = {
    "name": "sbx-n9kv-ao",
    "vendor": "cisco",
    "model": "Nexus9000 C9300v Chassis",
    "os": "nxos",
    "version": "9.3(3)",
    "ip": "10.1.1.1",
    1: "any data goes here",
}

print("\n")
print(f"device: {device}")
print(f"Device name: {device['name']}")

print("\n")
pp(device)

print("\n")
for key,value in device.items():
    print(f"{key:>16} : {value}")
    # print(f"{key:>16} : {value:>16}")
