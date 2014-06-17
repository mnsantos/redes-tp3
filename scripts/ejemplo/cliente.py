# Script que abre un socket y lo conecta al puerto 6677 de localhost.

import sys
import socket

sys.path.append('../../src/')
from ptc import Socket, SHUT_WR

to_send = 'foo bar baz'
received = str()
with Socket() as sock2:
	sock2.connect((sys.argv[1], 6677))
	sock2.send(to_send)
	received += sock2.recv(10)
	# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
	sock2.shutdown(SHUT_WR)
	received += sock2.recv(20)
print 'sock2 received: %s' % received