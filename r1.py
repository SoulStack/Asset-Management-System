from multiprocessing import Process
import main
import time

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1")

def f1():
  while True :
     try :
       if reader1.reader_status=="Connected" :
         print("Connected")
       else :
          print("waiting for connection")
          time.sleep(30)
     except :
      print("error on connecting reader")
def f2() :
    while True :
         try :
           tag = reader1.scan_tag_capture()
           print(tag)
         except :
             print("tag not scanned")
             pass
def f3():
    while True :
       try :
         insert = reader1.insert_into_activity()
         print(insert)
       except :
          print("Error in inserting")
          pass
if __name__ == "__main__" :
   a = Process(target = f1)
   b = Process(target = f2)
   c = Process(target = f3)
   a.start()
   b.start()
   c.start()
   a.join()
   b.join()
   c.join()
