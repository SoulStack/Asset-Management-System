from rfid_reader import RFIDReader
import time
# iniate
reader = RFIDReader('socket', host="192.168.0.250", port=27011, addr="00")
#connect
import time
reader.connect()
n=True
info = reader.getInfo()
print("INFO ", info)
while n==True:
	tags = reader.scantags()
	print(set(tags))
