import main1
from time import time ,sleep


#reader_ip = input("Enter Reader ip : ")
#port = input("Enter Port : ")
# mqtt_ip = input("Enter mqtt ip : ")
#reader_id = input("Enter Reader id : ")
#reader_location = input("Enter Reader Location : ")

reader1 = main1.Reader("10.0.175.93",6000,"10.0.175.122",678569,'10.0.175.122','SA','Soulsvciot01',"asset","campus20_room1")


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
            valid_tag_id = reader1.check_tag_id(tag1)
            if valid_tag_id == None :
                pass
            else:

                approve = reader1.check_approve_status(valid_tag_id)
                reader1.approval_status_mqtt(approve)
                print(approve)
                reader1.insert_into_Log(approve, valid_tag_id)
                reader1.change_movement_status(valid_tag_id, approve)
                reader1.check_tag_destination(valid_tag_id,approve) #it will change the movement status and approval status of the t>
                reader1.tag_alert_email(valid_tag_id,approve)
if __name__ == "__main__" :
    f1()

