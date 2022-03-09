import main
from time import time,sleep

reader1 = main.Reader("10.0.175.250",27011,"13.76.182.251","reader1",'10.0.175.122','SA','Soulsvciot01',"asset")

while True :
    sleep(5) #run the loop every one second
    tag = reader1.scan_tag_capture()
    if tag == None :
        pass
    else :
        tag1 = reader1.hex_to_string(tag)  # tag value return as bytes, hex_to_string function helps to convert that binary to hexadecimal string
        print(tag1) #just for acknowledgement
        print(type(tag1))
        approve = reader1.check_approve_status(tag1)
        reader1.insert_into_activity(approve,tag1)
