from rfid_reader import RFIDReader
from time import sleep
host = "10.0.175.250"
port = 27011
def scan_tag_capture():
        try:
            sleep(2)
            reader = RFIDReader('socket', host="10.0.175.250", port=27011, addr="00")
            reader.connect()
            info = reader.getInfo()
            tag = reader.scantag()
            return tag
        except :
            print("no tags scanned")

if __name__ == "__main__" :
    while True :
        sleep(2)
        scan_tag_capture()
