import main1
from time import time ,sleep
from functools import lru_cache
reader1 = main1.Reader("10.0.175.250",27011,"10.0.175.122",1357137,'10.0.175.122','SA','Soulsvciot01',"asset",213013)

@lru_cache(maxsize=400)
def f1() :
    while True :
        sleep(2)
        tag = reader1.scan_tag_capture()
        if tag == None:
            pass
        else:
            tag1 = reader1.hex_to_string(tag)  # tag value return as bytes, hex_to_string function helps to convert >            print(tag1)  # just for acknowledgement
            approve = reader1.check_approve_status(tag1)
            reader1.approval_status_mqtt(approve)
            print(approve)
            reader1.insert_into_Log(approve, tag1)
            reader1.check_tag_destination(tag1,approve) #it will change the movement status and approval status of t>
if __name__ == "__main__" :
    f1()
