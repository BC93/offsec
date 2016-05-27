
#! /usr/bin/env python
import commands
from scapy.all import *

base = "10.11.1." #IP range to scan minus the last octet.
f = open('snmp_output.txt', 'w+')
for i in range(1, 255):
    ip = base+str(i)
    print ip+"\n"
    p = IP(dst=ip)/UDP(dport=161, sport=39445)/SNMP(community="public",PDU=SNMPget(id=1416992799, varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.2.1.1.1.0"))]))
    pkt = sr1(p, timeout=1, iface='tap0')
    if pkt and pkt.sprintf("%IP.proto%") != "icmp":
        p1 = pkt.sprintf("%SNMP.PDU%").split("ASN1_STRING['", 1)
        p2 = p1[1].split("'", 1)
        print pkt.sprintf("%IP.src%")+" - "+p2[0]
        f.write(pkt.sprintf("%IP.src%")+" - "+p2[0]+"\n")
        f.close()
        print "\nDONE!!!!!!!!!!!!!!!\n"
