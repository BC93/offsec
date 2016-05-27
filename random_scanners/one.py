#!/usr/bin/python

"""
Just another scanner-type project I was working on...

I haven't worked on this one in a while and didn't comment anything or even know where I left off..I'm
Just uploading to github as a backup.

Software Requirements: Nmap, postgresql
pip requirements: psycopg2, libnmap
I think you'll also need to setup the database - as I didn't write a
script to make it. Maybe I'll upload one later.
For now I can just upload the database schema.

The target address range is hardcoded, You'll need to change the first 3 sections
of the ip to match you're target.
ex/ 192.168.1.

see line 185 to make this change.

Here's the schema for the database. hint I named the database offsec.

         List of relations
 Schema |   Name    | Type  | Owner
--------+-----------+-------+-------
 public | banners   | table | root
 public | hosts     | table | root
 public | http_dirs | table | root
 public | notes     | table | root
 public | services  | table | root


         Table "public.banners"
 Column |       Type        | Modifiers
--------+-------------------+-----------
 index  | character varying | not null
 banner | character varying |
Indexes:
    "banners_pkey" PRIMARY KEY, btree (index)

          Table "public.hosts"
 Column  |       Type        | Modifiers
---------+-------------------+-----------
 host    | character varying | not null
 s_index | character varying |
 os      | character varying |
Indexes:
    "hosts_pkey" PRIMARY KEY, btree (host)

        Table "public.http_dirs"
 Column |       Type        | Modifiers
--------+-------------------+-----------
 index  | integer           | not null
 host   | character varying |
 port   | integer           |
 dir    | character varying |
Indexes:
    "http_dirs_pkey" PRIMARY KEY, btree (index)

          Table "public.notes"
 Column |       Type        | Modifiers
--------+-------------------+-----------
 index  | integer           | not null
 host   | character varying |
 note   | character varying |
Indexes:
    "notes_pkey" PRIMARY KEY, btree (index)

         Table "public.services"
  Column  |       Type        | Modifiers
----------+-------------------+-----------
 index    | character varying | not null
 host     | character varying |
 port     | integer           |
 protocol | character varying |
 state    | character varying |
 service  | character varying |
Indexes:
    "services_pkey" PRIMARY KEY, btree (index)

create table services (index int primary key, host varchar, protocol varchar, port int, state varchar, service varchar);

create table notes (index int primary key, host varchar, note varchar);

"""
from libnmap.process import NmapProcess
from time import sleep
from libnmap.parser import NmapParser, NmapParserException
from libnmap.objects import service
from libnmap.objects import host as HOST
from psycopg2 import connect
import sys
from psycopg2 import extras
import random
from random import sample
from pprint import pprint as p
import db



ALPHNUM = ('1234567890')
def generate(count=1, length=12, chars=ALPHNUM):

    if count == 1:
            return ''.join(sample(chars,length))
    passwords = []
    while count > 0:
            passwords.append(''.join(sample(chars, length)))
            count -= 1
    return passwords


def store(host,  proto,port, state, serv, banner=None,  os=None, accuracy=None):

    index = generate(count=1, length=8)
    print index


    con = None
    con = connect(database='offsec')
    cur = con.cursor()
    # query = ("INSERT INTO services (host, protocol, port, state, service, banner) VALUES('{0}, {1}, {2}, {3}, {4}, {5}')".format(host,proto, port, state, serv, banner))
    try:
        query = ("select * from services   where( host='{}' AND protocol='{}' AND port='{}' AND state='{}' AND service='{}')").format(host,proto, port, state, serv)
        rows = cur.fetchall()
        print 'already in database...skipping'
        pass
    except:
        print "not in db...adding"
        if os == None:
            query = "INSERT INTO hosts (index, host) VALUES('{}','{}')".format(index, host)
            cur.execute(query)
        else:
            query = "INSERT INTO hosts (index, host, os, accuracy) VALUES('{}','{}', '{}', '{}')".format(index, host,  os, accuracy)
            cur.execute(query)
        query = "INSERT INTO services (index, protocol, port, state, service) VALUES('{}','{}','{}','{}','{}') ".format(index, proto, port, state, serv)
        cur.execute(query)
        if not banner == None:
            query = "insert into notes (index, host, note) values('{}','{}','{}')".format(index, host, banner)
            cur.execute(query)
            con.commit()
        else:
            query = "insert into notes (index, host) values('{}','{}')".format(index, host)
            cur.execute(query)
            con.commit()






# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run_background()
    while nmproc.is_running():
        print("Nmap Scan is running: ETC: {0} DONE: {1}%".format(nmproc.etc, nmproc.progress))
        sleep(2)
    print("rc: {0} output: {1}".format(nmproc.rc, nmproc.summary))

    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    con = None
    con = connect(database="offsec")
    cur= con.cursor()

    for host in nmap_report.hosts:
        if host.is_up():
            print("{0} {1}".format(host.address, " ".join(host.hostnames)))
            print("OS Fingerprint:")
            OS = []
            for osm in host.os.osmatches:
                OS.append((osm.name, osm.accuracy))
                os = OS[0][0]
                accuracy = OS[0][1]
            print os, accuracy
        if len(host.hostnames):
            tmphost = host.hostnames.pop()
        else:
            tmphost = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmphost,
            host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE")
        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            print '------------'
            addr = host.address
            proto = serv.protocol
            state = serv.state
            service = serv.service
            port = serv.port
            banner = serv.banner
            index= db.Index(addr, port)
            db.Host(index,addr,os=os)
            db.Service(index, addr, port, proto, state,service=service)
            db.Banner(index, banner)

            # store(addr, proto, port, state, service,  banner,  os, accuracy)
        # query = ("INSERT INTO services (host,porto, port, state, serv, banner) VALUES('{}, {},{}, {}, {}, {}')".format(host,proto, port, state, serv, banner))
            # print '------------'
            # print(pserv)
    # print(nmap_report.summary)

# def Service(index, host, port, protocol, state, service=None):
def loophosts():

        # args = "-n -Pn -T5 --max-retries=0 -O"


        g1 = [0,10]
        g2 = [3,54]
        h = raw_input("SET HOST: ")
        '''
        You'll have to set the TARGET address here...
        '''
        host = '192.168.13.{}'.format(h)
        a = raw_input("SET ARGS: ")
        args = "-O -n -vvvv -A -sV --max-retries 1  {}".format(a)
        # host = '192.168.13.2{}3'.format(g1[0])
        print host
        # report = do_scan(host, args)
        # if report:
        # print_scan(report)
        report = do_scan(host, args)
        print_scan(report)
        # else:
            # print("No results returned")
        # if report:
            # print_scan(report)
        # else:
            # print("No results returned")


# loophosts()
if __name__ == "__main__":

    loophosts()
