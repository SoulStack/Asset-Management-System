import main
from time import time,sleep 

reader1 = main.Reader("10.0.175.250",27011,"13.76.182.251","reader1",'10.0.175.122','SA','Soulsvciot01',"asset")

while True : 
	 sleep(10)
	 rdr_sts = reader1.reader_status()
	 print(rdr_sts)
	 
	 reader1.reader_status_mqtt(rdr_sts) #send the mqtt to the broker whether the reader is connected or disconnected

