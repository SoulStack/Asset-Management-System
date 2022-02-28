import main
import time
n=0
c=[]
reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")
while n<=10:
	b=reader1.scan_tag_capture()

	print(c)
	time.sleep(6)
	n+=1
print(reader1.reader_status())
