import main
from time import time ,sleep

reader1 = main.Reader("10.0.175.250",27011,"10.0.175.122",1357137,'10.0.175.122','SA','Soulsvciot01',"asset","campus12_lab1")

def f1() :
    while True :
        sleep(1)
        tag = reader1.scan_tag_capture()
        if tag == None:
            pass
        # elif tag == reader1.latest_from_logs():
        #     pass
        else:
            tag1 = reader1.hex_to_string(tag)   # tag value return as bytes, hex_to_string function helps to convert that into hexadecimal string
            print(tag1)
            # if tag1 == reader1.latest_from_logs():
            #     pass
            # else :
            valid_tag = reader1.check_tag(tag1)
            if valid_tag == None :
                pass
            else:

                approve = reader1.check_approve_status(tag1)
                reader1.approval_status_mqtt(approve)
                print(approve)
                reader1.insert_into_Log(approve, tag1)
                reader1.change_movement_status(tag1, approve)
                reader1.check_tag_destination(tag1,approve) #it will change the movement status and approval status of the t>
                reader1.tag_alert_email(tag1,approve)
if __name__ == "__main__" :
    f1()
