from rfid_reader import RFIDReader               #used to retrieve system information
import string
from time import  sleep#all time zones are available in this modu

reader = RFIDReader('socket', host="10.0.175.93" , port=6000, addr="00")

try:

    reader.connect()
    print("reader is now connected")
except:
    print("something went wrong..........")
def scan_tag():
    try :
        print("try block is executing")
        tags = reader.scantags()
        # a = [set(tags)]
        return  [set(tags)]
    except:
        print("except block is executing")
        return "unable to scan tag"

while True :

    scan_tag()
    sleep(2)
