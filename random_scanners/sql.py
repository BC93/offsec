from psycopg2 import connect
from tabulate import tabulate

'''

Selects all services for a given host.
Similar to using 'services {host}' in metasploit

'''
con = None
con = connect(database='offsec')
cur = con.cursor()
def hosts(cur):
    cur.execute('select host, os from hosts;')
    table = cur.fetchall()
    print tabulate(table, tablefmt='grid')


def services(cur):
    h = raw_input("Set Host: ")
    host = "192.168.13.{}".format(h)
    query = "select s.host, s.port, s.protocol, s.service, b.banner FROM services s, banners b WHERE(s.index=b.index AND s.host='{}')".format(host)
    print query
    cur.execute(query)
    table = cur.fetchall()
    print tabulate(table, tablefmt='grid')




services(cur)
# hosts(cur)

