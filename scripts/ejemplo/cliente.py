# Script que abre un socket y lo conecta al puerto 6677 de localhost.

import sys
import socket
import files
import tp_protocol
#from constantes import *

sys.path.append('../../src/')
from ptc import Socket, SHUT_WR
from ptc import protocol

received = str()

l = files.files_to_strings("../files/")

if len(sys.argv) >= 3:
    protocol.ACK_delay = float(sys.argv[2])
if len(sys.argv) >= 4:
    protocol.ACK_chance = float(sys.argv[3])

with Socket() as sock2: 
    sock2.connect((sys.argv[1], 6677))
    sock2.send(tp_protocol.SEND)
    data = sock2.recv(10)
    print "recibi algo: " + data
    msg = "hola mundo!"
    if data == tp_protocol.OK:
    	print "mando longitud de mensaje: " + str(len(msg))
    	sock2.send(str(len(msg)))
    	data = sock2.recv(10)
    	print "recibi algo: " + data
    	if data == tp_protocol.OK:
			print "mando mensaje: " + str(len(msg))
    		sock2.send(msg)
    #for i in l:
    #    sock2.send(i)
    # Cerramos el stream de escritura pero podemos seguir recibiendo datos.
    sock2.shutdown(SHUT_WR)
print 'sock2 received: %s' % received