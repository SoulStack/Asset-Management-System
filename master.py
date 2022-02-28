#write code here
from multiprocessing import Process
import main
import time
n=0
reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")

if __name__ == "__main__" :
   a = Process(target = reader1.reader_status)
   b = Process(target = reader1.scan_tag_capture)
   c = Process(target = reader1.insert_into_activity)

   a.start()
   b.start()
   c.start()

   a.join()
   b.join()
   c.join()
