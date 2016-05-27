
from psycopg2 import connect
con = None
con = connect(database='offsec')
cur = con.cursor()
def Host( index, host,os=None):
    con = None
    con = connect(database='offsec')
    cur = con.cursor()
    check = "SELECT host  FROM hosts WHERE(host='{}')".format(host)
    cur.execute(check)
    duplicates = cur.fetchall()
    if any(host in _host for _host in duplicates):
        print host
    else:
        print "Not already in database... adding"
        if os==None:
            print os
            print 'not listed'
            query = "INSERT INTO hosts (host, s_index) VALUES('{}', '{}')".format(host, index)
            cur.execute(query)
            con.commit()
        else:
            print "listed, ", os
            query = "INSERT INTO hosts (host, s_index, os) VALUES('{}', '{}', '{}')".format(host, index,os)
            print query
            cur.execute(query)
            con.commit()


# Host(cur, 1, '192.168.13.205')


def Service(index, host, port, protocol, state, service=None):
    con = None
    con = connect(database='offsec')
    cur = con.cursor()

    check = "SELECT port FROM services WHERE(services.host='{}' AND services.port='{}')".format(host,port)
    cur.execute(check)
    duplicates = cur.fetchall()
    print duplicates
    if any(port in _service for _service in duplicates):
        print service
    else:
        print "Service info not already in database... adding"
        if service==None:
            print service
            print 'Service not listed...'
            query = "INSERT INTO services (index, host, port, protocol, state) VALUES('{}','{}','{}','{}','{}')".format(index, host, port, protocol, state)
        else:
            print "Service is listed..."
            query = "INSERT INTO services (index, host, port, protocol, state, service) VALUES('{}','{}','{}','{}','{}','{}')".format(index, host, port, protocol, state, service)
        cur.execute(query)
        con.commit()


# Service(cur, 3, '192.168.13.204', 80, 'TCP', 'open','product: Microsoft IIS httpd version: 5.1 ostype: Windows')

def Banner(index, banner):

    con = None
    con = connect(database='offsec')
    cur = con.cursor()
    check = "SELECT  banner from banners where(index='{}')".format(index)
    cur.execute(check)
    duplicates = cur.fetchall()
    print duplicates
    if any(banner in _banner for _banner in duplicates):
        print index, banner
    else:
        check = "SELECT  index from banners where(index='{}')".format(index)
        cur.execute(check)
        duplicates = cur.fetchall()
        if any(index in _index for _index in duplicates):
            print "[*] DUPLICATE INDEX NUMBER...REPLACING OLD WITH NEW"
            # update = "UPDATE banners SET banner = '{}' WHERE index = '{}';".format(banner, index)
            delete = "DELETE FROM banners WHERE index = '{}'".format(index)
            cur.execute(delete)
            con.commit()
        print "Banner not already in database...adding"
        query = "INSERT INTO banners (index, banner) VALUES('{}','{}')".format(index, banner)
        cur.execute(query)
        con.commit()

def Index(host, port):
    print host, port
    ip = host.replace(".", "")
    index = "{}{}".format(ip,port)
    print index
    return index


