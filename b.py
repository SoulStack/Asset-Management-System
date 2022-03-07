import main
from time import time,sleep 

reader1 = main.Reader("192.168.0.250",27011,"13.76.182.251","reader1",'soulasset.database.windows.net','assetadmin','Soulsvciot01',"asset")

while True :
    sleep(1 - time() % 1) #run the loop every one second
    tag = reader1.scan_tag_capture()
    tag1 = reader1.hex_to_string(tag)  # tag value return as bytes, hex_to_string function helps to convert that binary to hexadecimal string
    print(tag1)
    print(type(tag1))
    reader1.insert_into_activity()
    
