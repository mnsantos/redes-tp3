# Script que abre un socket y lo conecta al puerto 6677 de localhost.

import sys
import socket
import files

sys.path.append('../../src/')
from ptc import Socket, SHUT_WR
from ptc import protocol

received = str()

#files.create_files()
l = files.files_to_strings("../files/")


if len(sys.argv) >= 3:
	protocol.ACK_delay = float(sys.argv[2])
if len(sys.argv) >= 4:
	protocol.ACK_chance = float(sys.argv[3])

with Socket() as sock2:	
	sock2.connect((sys.argv[1], 6677))
	j = 0
	for i in l:
		print j
		j = j+1
		sock2.send(i)
	received += sock2.recv(4000)
	# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
	sock2.shutdown(SHUT_WR)
print 'sock2 received: %s' % received