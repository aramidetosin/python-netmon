from pprint import pprint

device1_str = "  r3-L-n7, cisco, catalyst 2960, ios  "

print(device1_str.split(','))
device1 = device1_str.split(',')
print(device1[0].lstrip())

print(device1_str.strip().split(','))


device1 = device1_str.replace(" ", "").split(",")
print(device1)

device1 = device1_str.replace(" ", "").replace(",", ":")
print(device1)

version = "Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.11.1a, RELEASE SOFTWARE (fc1)"
expected_version = "Version 16.11.1a"

index = version.find(expected_version)
print(f"found version: {expected_version} at location {index} ")
print(version[index:])


version_info = version.split(",")
for part_no, version_info_part in enumerate(version_info):
    print(f"version part {part_no}: {version_info_part.strip()}")

show_interface_stats = """
GigabitEthernet1
          Switching path    Pkts In   Chars In   Pkts Out  Chars Out
               Processor      25376    1529598       8242     494554
             Route cache          0          0          0          0
       Distributed cache     496298   60647894     673003  218461079
                   Total     521674   62177492     681245  218955633
GigabitEthernet2
          Switching path    Pkts In   Chars In   Pkts Out  Chars Out
               Processor         19       1140          0          0
             Route cache          0          0          0          0
       Distributed cache       6077     663304          0          0
                   Total       6096     664444          0          0
Interface GigabitEthernet3 is disabled
Loopback21
          Switching path    Pkts In   Chars In   Pkts Out  Chars Out
               Processor          0          0          0          0
             Route cache          0          0          0          0
       Distributed cache          0          0          0          0
                   Total          0          0          0          0
Loopback55
          Switching path    Pkts In   Chars In   Pkts Out  Chars Out
               Processor          0          0          3        241
             Route cache          0          0          0          0
       Distributed cache          0          0          0          0
                   Total          0          0          3        241
Loopback100
          Switching path    Pkts In   Chars In   Pkts Out  Chars Out
               Processor          0          0         43       2806
             Route cache          0          0          0          0
       Distributed cache          0          0          0          0
                   Total          0          0         43       2806
"""
from pprint import pprint
interface_counters = dict()
show_interface_stats_lines = show_interface_stats.splitlines()
# pprint(show_interface_stats_lines)
for index, stats_line in enumerate(show_interface_stats_lines):
    if stats_line.find('GigabitEthernet', 0) == 0:

        totals_line = show_interface_stats_lines[index + 5]
        interface_counters[stats_line] = totals_line.split()[1:]

print("\n\n----- Interface Counters --------------------")
pprint(interface_counters)

show_arp = """
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.10.20.48             -   0050.56bb.e99c  ARPA   GigabitEthernet1
Internet  10.10.20.200           14   0050.56bb.8be2  ARPA   GigabitEthernet1
Internet  10.10.20.254            0   0896.ad9e.444c  ARPA   GigabitEthernet1
"""

arp_table = dict()
for arp_line in show_arp.splitlines():
    if arp_line.lower().find("internet", 0) == 0:
        arp_table[arp_line[10:25].strip()] = arp_line[38:52]

pprint(arp_table)



xx = "GigabitEthernet1".find("GigabitEthernet1", 0) == 0
print(xx)