import main
from time import time,sleep 
from functools import lru_cache
 #maxsize means how many results can it store at a time and ttl means how much time a result have to live

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1",'soulasset.database.windows.net','assetadmin','Soulsvciot01',"asset")

@lru_cache(maxsize = 100)
def f1():
   while True :
         sleep(1)
         tag = reader1.scan_tag_capture()
         tag1 = reader1.hex_to_string(tag)
         print(tag1)
         if tag1 == None :
               pass
         else :
              approve = reader1.check_approve_status(tag1)
              print(approve)
              reader1.approval_status_mqtt(approve)

if __name__ == "__main__":
    f1()
