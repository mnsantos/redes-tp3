# Script que liga un socket al puerto 6677 de localhost.

import sys

sys.path.append('../../src/')
from ptc import Socket
from ptc import protocol

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

to_send = 'a'*3000
print sys.getsizeof(to_send)
received = str()

if len(sys.argv) >= 2:
    protocol.ACK_delay = float(sys.argv[1])
if len(sys.argv) >= 3:
    protocol.ACK_chance = float(sys.argv[2])

with Socket() as sock1:    
	print get_lan_ip()
	sock1.bind((get_lan_ip(), 6677))
	sock1.listen()
	sock1.accept()
	received += sock1.recv(6000)
	sock1.send(to_send)
	sock1.close()
print 'sock1 received: %s' % received