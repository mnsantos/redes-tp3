# Script que liga un socket al puerto 6677 de localhost.

import sys

sys.path.append('/home/martin/Documentos/redes/redes-tp3/src/ptc/')
from ptc import Socket

to_send = 'Lorem ipsum dolor sit amet'
received = str()
with Socket() as sock1:
	sock1.bind(('127.0.0.1', 6677))
	sock1.listen()
	sock1.accept()
	received += sock1.recv(15)
	sock1.send(to_send)
	sock1.close()
print 'sock1 received: %s' % received