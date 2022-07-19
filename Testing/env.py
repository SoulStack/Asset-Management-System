import main
from time import time, sleep
import os 
user_name = os.environ.get('db_user_name')
password = os.environ.get('db_pwd')
print(user_name,password)
reader1 = main.Reader("10.2.96.91",27011,"10.0.2.19",678569,'10.0.2.19',user_name,password,"asset",781013)




def f1() :
    while True :
        sleep(0.5)
        tags = reader1.scan_tag_capture()
        if tags == None:
            pass
        else:
            for i in tags :
                tag_uuid = reader1.hex_to_string(i)   # tag value return as bytes, hex_to_string function helps to convert that into hexadecimal string
                print(tag_uuid)
                if tag_uuid == None:
                    pass
                else :
                    tag_id = reader1.check_tag_id(tag_uuid)
                    print(tag_id)
                    tag_location = reader1.check_tag_location(tag_id)
                    print("current tag location_id is >>>>",tag_location)
                    if tag_id == None :
                        pass
                    else :

                        tag_id_in_activity = reader1.check_tag_in_activity(tag_id)
                    # print(tag_id_in_activity)
                    # if tag_location == reader1.room_name :

                        if tag_id == tag_id_in_activity : #checking the same tag is present in activity or not
                            approve = reader1.check_approve_status(tag_id)
                            print(approve)
                            if approve == "Approved" :

                                reader1.insert_into_Log(approve, tag_id)
                                reader1.change_movement_status(tag_id, approve)
                                reader1.check_tag_destination(tag_id,approve)  # it will change the movement status and approval status of the t>
                        # reader1.tag_alert_email(tag_id, approve)
                            else :
                                reader1.send_mqtt_to_display(tag_id,approve)
                                reader1.insert_into_alert(tag_id)
                        else :
                            approve = reader1.check_approve_status(tag_id)
                            print(approve)
                            reader1.send_mqtt_to_display(tag_id, approve)
                            reader1.insert_into_alert(tag_id)


if __name__ == "__main__" :
    f1()

