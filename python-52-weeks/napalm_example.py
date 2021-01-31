import napalm
import json


print("\n----- connecting to device (SSH) ----------")
driver = napalm.get_network_driver('ios')
with driver(hostname='192.168.1.231',
            username='admin',
            password='juniper1',
            ) as device:

    print("\n----- facts ----------")
    print(json.dumps(device.get_facts(), sort_keys=True, indent=4))

    print("\n----- interfaces ----------")
    print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))

    print("\n----- vlans ----------")
    print(json.dumps(device.get_vlans(), sort_keys=True, indent=4))

    print("\n----- snmp ----------")
    print(json.dumps(device.get_snmp_information(), sort_keys=True, indent=4))

    print("\n----- interface counters ----------")
    print(json.dumps(device.get_interfaces_counters(), sort_keys=True, indent=4))

    print("\n----- environment ----------")
    print(json.dumps(device.get_environment(), sort_keys=True, indent=4))


print("\n----- connecting to device (IOS-XR) ----------")
driver = napalm.get_network_driver('iosxr')
with driver(hostname='192.168.1.221',
            username='admin',
            password='admin',
            # optional_args={'port': 10000}) as device:
            ) as device:

    print("\n----- facts ----------")
    print(json.dumps(device.get_facts(), sort_keys=True, indent=4))

    print("\n----- interfaces ----------")
    print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))

    print("\n----- snmp ----------")
    print(json.dumps(device.get_snmp_information(), sort_keys=True, indent=4))


print("\n----- connecting to device (vSRX) ----------")
driver = napalm.get_network_driver('junos')
with driver(hostname='192.168.1.226',
            username='admin',
            password='juniper1',
            ) as device:

    print("\n----- facts ----------")
    print(json.dumps(device.get_facts(), sort_keys=True, indent=4))

    print("\n----- interfaces ----------")
    print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))

    print("\n----- interface counters ----------")
    print(json.dumps(device.get_interfaces_counters(), sort_keys=True, indent=4))
