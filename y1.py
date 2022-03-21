import main
from time import time ,sleep
from functools import lru_cache
reader_ip = input("enter reader ip : ")
port =int(input("enter port : "))
mqtt_ip = input("enter mqtt ip : ")
reader_id = input("enter reader id : ")
reader_location = input("enter reader location : ")

reader1 = main.Reader(reader_ip,port,mqtt_ip,reader_id,'10.0.175.122','SA','Soulsvciot01',"asset",reader_location)

@lru_cache(maxsize=400)
def f1() :
    while True :
        sleep(4)
        tag = reader1.scan_tag_capture()
        if tag == None:
            pass
        else:
            tag1 = reader1.hex_to_string(tag)
            print(tag1)# tag value return as bytes, hex_to_string function helps to convert that into hexadecimal string
            approve = reader1.check_approve_status(tag1)
            reader1.approval_status_mqtt(approve)
            print(approve)
            reader1.insert_into_Log(approve, tag1)
            reader1.check_tag_destination(tag1,approve) #it will change the movement status and approval status of the tag
if __name__ == "__main__" :
    f1()


