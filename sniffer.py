from scapy.all import *

packets = sniff(iface='tap0', count='1000')

with open('packets.cap','w') as f:
    f.write(packets)
