from subprocess import call
from threading import Thread
from psycopg2 import connect
from requests import request


'''

I think this module is supposed to be similar to dirbuster. Considering it uses dirb's wordslists.
No idea.

'''

def get_hosts():
    con = None
    con = connect(database="offsec")
    cur = con.cursor()

    query = "SELECT host, service, banner  FROM services, banners WHERE port=80 AND banners.index = services.index"
    cur.execute(query)
    hosts = cur.fetchall()
    # print hosts
    return brute_force(hosts)

def dirb(host):
    #...
    cmd = "dirb"
    target = "http://{}/".format(host[0][0])
    results = call("{} {} -r".format(cmd, target), shell=True)
    print results

def brute_force(hosts):
    for host in hosts:
        banner = host[2]
        host = host[0]
        print host
        base = 'http://{}/'.format(host)
        services = [('iis', '/usr/share/wordlists/dirb/vulns/iis.txt'), ('apache','/usr/share/wordlists/dirb/vulns/apache.txt'), ('tomcat', '/usr/share/wordlists/dirb/vulns/tomcat.txt')]
        key_words = banner.lower().split()
        extensions = ['.asp', 'php', 'html']
        for index, list in enumerate(services):
            word = list[0]
            if any(word in _word for _word in key_words):
                print word, key_words
                wordlist = services[index][1]
                wl = open(wordlist).readlines()
                print wl

            # else:
                # print word, key_words
        # print key_words


        # print wordlist
                dirs = []
                for word in wl:
                    url = base+word
                    print url
                    load = request(method="GET", url=url)
                    print word, load.status_code, load.reason
                    if load.status_code == 200:
                        dirs.append(url)
                    if load.status_code == 403:
                        dirs.append(url)
                    # for ext in extensions:
                        # print ext
                        # url2 = base+word+ext
                        # print url2
                        # load = request(method="GET", url=url2)
                        # print url2, load.status_code, load.reason


                    # if load.status_code == 404:
                        # pass
                    # else:
                    # print word, load.status_code
        print dirs


if __name__ == "__main__":
    get_hosts()
