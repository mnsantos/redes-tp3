# Script que abre un socket y lo conecta al puerto 6677 de localhost.
import sys
import socket
import files
import tp_protocol
import time
import threading
import random
#from constantes import *

class Info:
    def __init__(self):
        self.troughput=0
        self.retransmissions=0
        self.drops=0

sys.path.append('../../src/')
from ptc import Socket, SHUT_WR
from ptc import protocol

received = str()

l = files.files_to_strings("../files/")

if len(sys.argv) >= 3:
    protocol.ACK_delay = float(sys.argv[2])
if len(sys.argv) >= 4:
    protocol.ACK_chance = float(sys.argv[3])
#protocol.droppedPackets = 0

ts = []

def change_delay():
	protocol.ACK_delay = random.random() * 0.13 + 0.02	
	global stopTimer
	if not stopTimer:
		timer = threading.Timer(0.01, change_delay)	
		timer.start()
timer = threading.Timer(0.01, change_delay)    
timer.start()

stopTimer = False

with Socket() as sock2: 
    sock2.connect((sys.argv[1], 6677))
    for i in l:
        h = Info()
        sock2.send(tp_protocol.SEND)
        data = sock2.recv(10)
        if data == tp_protocol.OK:
            #print "mando longitud de mensaje: " + str(len(i))
            start = time.time()
            sock2.send(str(len(i)))
            data = sock2.recv(10)
            #print "recibi algo: " + data
            if data == tp_protocol.OK:
                #print "mando mensaje: " + i
                sock2.send(i)
                data = sock2.recv(10)
                if data == tp_protocol.END:
                    end = time.time()
                    print "Start: "+str(start)
                    print "End: "+str(end)
                    h.troughput = (len(i)/(end-start))/1024
    sock2.send(tp_protocol.EXIT)

    print h.troughput
    sock2.shutdown(SHUT_WR)
stopTimer = True