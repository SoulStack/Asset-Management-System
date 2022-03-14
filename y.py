import main
from time import time ,sleep
from functools import lru_cache
reader1 = main.Reader("10.0.175.250",27011,"10.0.175.122","reader1",'10.0.175.122','SA','Soulsvciot01',"asset")

@lru_cache(maxsize=100)
def f1() :
    while True :
        sleep(5)
        rdr_sts = reader1.reader_status()
        print(rdr_sts)
        reader1.reader_status_mqtt(rdr_sts)
        sleep(5)
        tag = reader1.scan_tag_capture()
        if tag == None:
            pass
        else:
            tag1 = reader1.hex_to_string(tag)  # tag value return as bytes, hex_to_string function helps to convert that binary to hexadecimal string
            print(tag1)  # just for acknowledgement
            print(type(tag1))
            approve = reader1.check_approve_status(tag1)
            print(approve)
            reader1.insert_into_activity(approve, tag1)
            reader1.approval_status_mqtt(approve)

if __name__ == "__main__" :
    f1()
