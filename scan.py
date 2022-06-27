import time
import re
from rfid_reader import RFIDReader
import codecs
import time
import string

reader = RFIDReader('socket', host="10.0.175.239", port=27011, addr="00")
reader.connect()
info = reader.getInfo()
print("INFO ", info)
# scan single tag
# tag = reader.scantag()
# tags = reader.scantags()
data = []
data1 = []

while True:
    time.sleep(2)
    scanned_tags = reader.scantags()
    print(type(scanned_tags))
    # tags1 = re.findall("31\w{22}", tags[0])
    tags = set(scanned_tags)
    tags1 = list(tags)
    print('tag', tags1)
    #for i in range(len(tags)):
        #binary_str = codecs.decode(tags[i], "hex")
        #print("tag_uuid ",str(binary_str, 'utf-8'))
    for i in tags1 :
        binary_string = codecs.decode(i,"hex")
        print(binary_string)
        print("length of string is ",len(binary_string))
        tag_uuid = binary_string[:]
        #data.append(tag_uuid)
    #print("list of tag_uuid are ", data)
