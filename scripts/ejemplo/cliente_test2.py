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
        self.throughput=0
        self.retransmissions=0
        self.drops=0
        self.fileSize=0
        self.timeAvg=0
        self.runsCount=0
        self.delay=0
        self.drops=0

sys.path.append('../../src/')
from ptc import Socket, SHUT_WR
from ptc import protocol

received = str()

l = files.files_to_strings("../files/")

#if len(sys.argv) >= 3:
#    protocol.ACK_delay = float(sys.argv[2])
#if len(sys.argv) >= 4:
#    protocol.ACK_chance = float(sys.argv[3])

#protocol.droppedPackets = 0

ts = []

stopTimer = False

def change_delay():
	protocol.ACK_delay = random.random() * 0.13 + 0.02	
	global stopTimer
	if not stopTimer:
		timer = threading.Timer(0.01, change_delay)	
		timer.start()

def change_drop():
    protocol.ACK_chance = random.random() * 0.02 + 0.98   
    global stopTimer
    if not stopTimer:
        timer = threading.Timer(0.01, change_drop) 
        timer.start()

#timer = threading.Timer(0.01, change_delay)    
#timer.start()

timer = threading.Timer(0.01, change_drop)  
timer.start()

protocol.ACK_delay = 0
#ACKs = [0.01, 0.02, 0.03, 0.04, 0.05]
ACKs = [0.075, 0.1]

tests = []
with Socket() as sock2: 
    sock2.connect((sys.argv[1], 6677))    
    for i in l:        
        #print "\nRunning file: " + str(len(i)/1024) + "kb" 
        for k in range(0, len(ACKs)):            
            h = Info()        
            h.runsCount = 3        
            h.delay = ACKs[k]
            protocol.ACK_delay = h.delay       
            #print "Using delay: " + str(protocol.ACK_delay)
            protocol.droppedPackets = 0
            for j in range(0, h.runsCount):            
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
                            #print "time: "+str(end-start)                        
                            h.timeAvg += end-start            
            h.timeAvg /= h.runsCount
            #print "timeAvg: " + str(h.timeAvg)
            h.fileSize = len(i)/1024
            h.throughput = h.fileSize/h.timeAvg
            h.drops = protocol.droppedPackets/h.runsCount
            tests.append(h)
    sock2.send(tp_protocol.EXIT)

    for i in range(0, len(tests)):
        h = tests[i]
        print "[Test " + str(i) + "] throughput:" + str(h.throughput) + "kb/s, fileSize:" + str(h.fileSize) + "kb, timeAvg:" + str(h.timeAvg) + "s, delay:" + str(h.delay)

    with open("output.json", 'w') as f:
        f.write("[\n");
        for i in range(0, len(tests)):
            h = tests[i]
            f.write("{")
            f.write('"throughput":"' + str(h.throughput) + '","fileSize":"'+ str(h.fileSize) + '", "timeAvg":"' + str(h.timeAvg) + '", "delay":"' + str(h.delay) + '", "drops":"' + str(h.drops) + '"') 
            f.write("}")
            if i < len(tests)-1:
                f.write(",")            
            f.write("\n")
        f.write("]")

    sock2.shutdown(SHUT_WR)
stopTimer = True
