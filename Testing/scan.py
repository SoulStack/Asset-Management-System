import time
import re
from rfid_reader import RFIDReader
import codecs
import time
import string

reader = RFIDReader('socket', host="10.0.160.194", port=27011, addr="00")
reader.connect()
info = reader.getInfo()
print("INFO ", info)
# scan single tag
# tag = reader.scantag()
# tags = reader.scantags()
#data = []
#data1 = []
#import pyodbc as py
#db_servername = "10.0.2.19"
#db_database = "asset"
#db_username = "SA"
#db_password= "Soulsvciot01"
#cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
#cursor = cnxn.cursor()


while True:
    time.sleep(2)
    scanned_tags = reader.scantags()
    print(type(scanned_tags))
    # tags1 = re.findall("31\w{22}", tags[0])
    tags = list(set(scanned_tags))
    print('tag', tags)
    #for i in range(len(tags)):s
        #binary_str = codecs.decode(tags[i], "hex")
        #print("tag_uuid ",str(binary_str, 'utf-8'))
    for i in tags :
        binary_string = codecs.decode(i,"hex")
        print(binary_string)
        print("length of string is ",len(binary_string))
       # cursor.execute("SELECT tag_id FROM tags WHERE tag_uuid = (?)",(binary_string))
       # value = cursor.fetchone()
       # print(value)
        
        
