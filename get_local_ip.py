import socket

def main():
    ''' Creates our socket'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ''' Can connect to whatever we want, just using gmail since it's easy '''
    s.connect(('gmail.com',80))

    ''' Gets our private IP Address '''
    host = s.getsockname()[0]

    ''' Always close the connection'''
    s.close()

    ''' Now just formatting, stripping, and crafting our subnet'''
    g = host.split('.')
    subnet = '{}.{}.{}.1/24'.format(g[0],g[1], g[2])
    print subnet
    return subnet

if __name__=="__main__":
    main()
