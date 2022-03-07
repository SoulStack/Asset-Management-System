import main
from time import time,sleep 

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")

while True : 
	 rdr_sts = reader1.reader_status()
	 sleep(10)
	 print(rdr_sts)
	 sleep(10)
	 reader1.reader_status_mqtt(rdr_sts) #send the mqtt to the broker whether the reader is connected or disconnected

