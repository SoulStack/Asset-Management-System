from rfid_reader import RFIDReader
# iniate
reader = RFIDReader('socket', host="192.168.0.250", port=27011, addr="00")
#connect

reader.connect()
info = reader.getInfo()
print("INFO ", info)
#scan single tag
tag = reader.scantag()
tags = reader.scantags()

print('tag', tag)
print('tags', tags)
name=bytes.fromhex(tag)
ascii_string = name.decode("ASCII")
print(ascii_string)
