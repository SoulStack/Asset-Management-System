import main
import time
n=0
reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")
while True:
	b=reader1.scan_tag_capture()
	print(map(reader1.hex_to_string,b))
	#time.sleep(1)
