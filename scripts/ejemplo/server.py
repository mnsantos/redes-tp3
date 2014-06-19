# Script que liga un socket al puerto 6677 de localhost.

import sys
#from constantes import *
import tp_protocol

sys.path.append('../../src/')
from ptc import Socket
from ptc import protocol
from ptc import constants

import os
import socket

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

to_send = 'a'*10
#print sys.getsizeof(to_send)

if len(sys.argv) >= 2:
    protocol.ACK_delay = float(sys.argv[1])
if len(sys.argv) >= 3:
    protocol.ACK_chance = float(sys.argv[2])
#protocol.droppedPackets = 0

with Socket() as sock1:
    print "Server running on: " + get_lan_ip()
    sock1.bind((get_lan_ip(), 6677))
    sock1.listen()
    sock1.accept()
    
    while True:
        data = sock1.recv(10)
        #print "recibi algo: " + data
        if data == tp_protocol.SEND:
            #print "mando ok: "
            sock1.send(tp_protocol.OK)
            numBytes = int(sock1.recv(10))
            #print "recibi numBytes: " + str(numBytes)
            #print "mando ok: "
            sock1.send(tp_protocol.OK)
            BUFF_SIZE = constants.RECEIVE_BUFFER_SIZE
            fullBuffsCount = numBytes/BUFF_SIZE
            remainingBytes = numBytes % BUFF_SIZE
            data = ""
            for i in range(0, fullBuffsCount):
                data += sock1.recv(BUFF_SIZE)
            if remainingBytes > 0:
                data += sock1.recv(remainingBytes)
            sock1.send(tp_protocol.END)
            file = open("../received/_"+str(numBytes), "w")
            file.write(data)
        if data == tp_protocol.EXIT:
            break
    sock1.close()

    
    #for i in range(0,FILES_TO_SEND):
    #    data = sock1.recv(BUFFER_SIZE)
    #    file = open("../files/_"+str(i), "w")
    #        sock1.close()