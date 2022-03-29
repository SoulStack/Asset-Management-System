import main
from time import time ,sleep
from cachetools import cached, TTLCache
# from functools import lru_cache
# reader_ip = input("Enter Reader ip : ")
# port = input("Enter Port : ")
# mqtt_ip = input("Enter mqtt ip : ")
reader_id = input("Enter Reader id : ")
reader_location = input("Enter Reader Location : ")

reader1 = main.Reader("10.0.166.20",6000,"10.0.175.122",reader_id,'10.0.175.122','SA','Soulsvciot01',"asset",reader_location)

# @lru_cache(maxsize=1000)
cache = TTLCache(maxsize=100, ttl=86400)

@cached(cache)
def f1() :
    while True :
        sleep(1)
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
            reader1.change_movement_status(tag1,approve)
            reader1.check_tag_destination(tag1,approve) #it will change the movement status and approval status of the tag
            reader1.tag_alert_email(tag1,approve)

if __name__ == "__main__" :
    f1()
