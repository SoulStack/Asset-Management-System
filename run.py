from multiprocessing import multiprocessing
import main
import time

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")

if __name__ =="__main__":
	while True:
		try:
			if reader1.reader_status() =="Connected":
				print("Connecting")
			else:
				print("Reader not connected")
				time.sleep(2)
				print("Waiting... please connect in 30s")
				time.sleep(30)
		except Exception as e:
			raise
		else:
			print("error on connecting reader")
		finally:
			a = Process(target = reader1.reader_status)
			b = Process(target = reader1.scan_tag_capture)
			c = Process(target = reader1.insert_into_activity)

			a.start()
			b.start()
			c.start()
			a.join()
			b.join()
			c.join()
