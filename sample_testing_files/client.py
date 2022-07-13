import codecs
import socket
import threading
import json
import hashlib
from subprocess import PIPE, Popen
s= socket.socket()

port =27011

s.connect(("192.168.0.250",port))

data=s.recv(1024)
data=codecs.encode(data,'hex')
print(data)

s.close()
