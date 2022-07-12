import pyodbc as py
import string
import csv

db_servername='10.0.2.19'
db_database='asset'
db_username='SA'
db_password='Soulsvciot01'

cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)

list2=[]
with open("/home/u_admin/RFID TAG DETAILS - ICT(1).csv",'r',encoding="utf-8") as file:
    reader = csv.reader(file)
    header=next(reader)
    for row in reader:
        list2.append(row)

def value_insrt():
    for i in list2:
        asset_id=i[4]
        tag_uuid=i[1]
        cursor = cnxn.cursor()
        if tag_uuid==None:
            pass
        else:
            cursor.execute("""INSERT INTO tags(tag_uuid,dept_id)values(?,3)""",tag_uuid)
    cnxn.commit()

value_insrt()
