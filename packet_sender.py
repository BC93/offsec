#!/usr/bin/python
from scapy.all import *
ip=IP(src='10.0.0.26', dst='10.0.0.169')
SYN=TCP(sport=1030, dport=80, flags="S", seq=12345)
SYNACK=sr1(ip/SYN)
my_ack = SYNACK.seq + 1
ACK=TCP(sport=1030, dport=80, flags="A", seq=11, ack=my_ack)
payload="SENDTCP"
PUSH=TCP(sport=1030,dport=80, flags="PA", seq=11, ack=my_ack)
packets = sr1(ip/PUSH/payload)

