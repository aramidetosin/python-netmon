from collections import namedtuple

Device = namedtuple('xxx', ['name', 'vendor', 'model', 'os', 'ip'])
device = Device('lhr54-br-agg-r1', 'cisco', 'Nexus 9000v chassis', 'nxos', '10.1.1.1')

print(f"name: {device.name}")
print(f"name: {device.vendor}")
print(f"name: {device.model}")