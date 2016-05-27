from scapy.all import *
from pprint import pprint
from psycopg2 import connect

network = '10.0.0.0/24'
def arp_sweep(network):
    arp_sweep = arping(net=network)
    return arp_sweep
a = arp_sweep(network)
caps = []
strings = []
for cap in enumerate(a[0]):
    caps.append(cap[1])
    for x in enumerate(caps):
        for y in enumerate(x):
            strings.append(y[1])
for string in strings:
    stripped = str(string).strip(',')
ls = []

for x,y in enumerate(caps):
    ls.append(caps[x])
ips = {}
macs = []
for index, ip in enumerate(ls):
    ip =str(ls[index]).format().strip()[54:64].rstrip('|').rstrip(' ')
    ips[str(ls[index]).format().strip()[54:64].rstrip('|').rstrip(' ')] = ''
    mac = str(ls[index]).format().strip()[102:121].rstrip('|').rstrip(' ')
    m = mac.format().split(' ')[0]
    if '=' in m:
       m =  m.split('=')[1]
    macs.append(m)
    ips[ip] = m
pprint(ips)


arp_sniff = sniff(filter="arp",count=10).summary()
print arp_sniff


class db():
    def __self__():
        self
    def con(self):
        con = connect(database='msf', user='root', password='B@11os.L23')
        cur = con.cursor()
        cur.execute('select * from hosts;')
        hosts = cur.fetchall()
        print hosts

k = db()
k.con()
