

import main
from time import time ,sleep

reader1 = main.Reader("10.0.160.95",6000,"10.0.2.19",678569,'betapoint.database.windows.net','ams','Soulsvciot01',"btams",781013)


def f1() :
    while True :
        sleep(1)
        tag = reader1.scan_tag_capture()
        if tag == None:
            pass
        else:
            tag1 = reader1.hex_to_string(tag)   # tag value return as bytes, hex_to_string function helps to convert tha>
            print(tag1)
            if tag1 == None:
                pass
            else :
                tag_id = reader1.check_tag_id(tag1)
                print(tag_id)
                tag_location = reader1.check_tag_location(tag_id)
                print("current tag location_id is >>>>",tag_location)
                if tag_id == None :
                    pass
                else :

                    tag_id_in_activity = reader1.check_tag_in_activity(tag_id)
                    if tag_id == tag_id_in_activity : #checking the same tag is present in activity or not
                        approve = reader1.check_approve_status(tag_id)
                        print(approve)
                        if approve == "Approved" :

                            reader1.insert_into_Log(approve, tag_id)
                            reader1.change_movement_status(tag_id, approve)
                            reader1.check_tag_destination(tag_id,approve)  # it will change the movement status and appr>
                        # reader1.tag_alert_email(tag_id, approve)
                        else :
                            reader1.send_mqtt_to_display(tag_id,approve)
                            reader1.insert_into_alert(tag_id)
                            # reader1.tag_alert_email(tag_id,approve)
                    else :
                        approve = reader1.check_approve_status(tag_id)
                        print(approve)
                        reader1.send_mqtt_to_display(tag_id, approve)
                        reader1.insert_into_alert(tag_id)
                        # reader1.tag_alert_email(tag_id, approve)


if __name__ == "__main__" :
    f1()



