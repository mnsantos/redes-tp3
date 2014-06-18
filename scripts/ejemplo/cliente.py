# Script que abre un socket y lo conecta al puerto 6677 de localhost.

import sys
import socket

sys.path.append('../../src/')
from ptc import Socket, SHUT_WR
from ptc import protocol

to_send = 'foo bar baz'
received = str()

if len(sys.argv) >= 3:
	protocol.ACK_delay = float(sys.argv[2])
if len(sys.argv) >= 4:
	protocol.ACK_chance = float(sys.argv[3])

with Socket() as sock2:	
	sock2.connect((sys.argv[1], 6677))
	for i in range(0,100):
		sock2.send(to_send)
	received += sock2.recv(4000)
	# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
	sock2.shutdown(SHUT_WR)
print 'sock2 received: %s' % received