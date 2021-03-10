import pyshark

# CAPTURE EVERYTHING AND PRINT PACKET SUMMARIES
print("\n----- Packet summaries --------------------")
capture = pyshark.LiveCapture(interface='wlp0s20f3', only_summaries=True)
capture.sniff(packet_count=20)
for packet in capture:
    print(f"    {packet}")

# CAPTURE DNS AND PRINT PACKETS
print("\n----- DNS packet summaries --------------------")
capture = pyshark.LiveCapture(interface='wlp0s20f3', only_summaries=True, bpf_filter='udp port 53')
capture.sniff(packet_count=20)
for packet in capture:
    print(f"    {packet}")

# CAPTURE AND PRINT COMPLETE PACKETS
print("\n\n----- All packets, complete ---------------------")
capture = pyshark.LiveCapture(interface='wlp0s20f3')
capture.sniff(packet_count=20)
for packet in capture:
    print(packet)

# CAPTURE AND HANDLE PACKETS AS THEY ARRIVE
print("\n\n----- Print packets as they are detected ---------------------")
capture = pyshark.LiveCapture(interface='wlp0s20f3', only_summaries=True, bpf_filter='tcp port https')


def print_packet(pkt):
    print("    ", pkt)


capture.apply_on_packets(print_packet, packet_count=20)


# CAPTURE AND HANDLE PACKETS AS THEY ARRIVE USING LAMBDA
print("\n\n----- Print packets as they are detected (lambda version) ---------------------")
capture = pyshark.LiveCapture(interface='wlp0s20f3', only_summaries=True, bpf_filter='tcp port https')
capture.apply_on_packets(lambda pkt: print("lambda    ", pkt), packet_count=20)


# CAPTURE AND HANDLE PACKETS AS THEY ARRIVE USING SNIFF CONTINUOUSLY()
print("\n\n----- Print packets as they are detected sniff_continuously() version) ---------------------")
capture = pyshark.LiveCapture(interface='wlp0s20f3', only_summaries=True, bpf_filter='tcp port https')
for packet in capture.sniff_continuously(packet_count=10):
    print_packet(packet)

#ALLOW USER TO ENTER BPF FILTER
while True:

    bpf_filter = input("\n\nEnter BPF filter: ")
    if not bpf_filter:
        break

    print(f"\n----- capturing packets with BPF filter: {bpf_filter}")
    capture = pyshark.LiveCapture(interface='wlp0s20f3', only_summaries=True, bpf_filter=bpf_filter)
    try:
        capture.apply_on_packets(print_packet, packet_count=20)
    except KeyboardInterrupt as e:
        continue