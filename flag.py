import pyodbc as py
import string
import csv

db_servername='10.0.2.19'
db_database='asset'
db_username='soul_admin'
db_password='Soulams.svciot'

cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)

list2=[]
with open("/home/u_admin/RFID  TAG DETAILS - Sheet4.csv",'r',encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        list2.append(row)


def value_insrt():
    for i in list2:
        asset_id=i[3]
        tag_uuid=i[1]
        asset_name=i[4]
        print(asset_id)
        cursor = cnxn.cursor()
        if tag_uuid==None:
            pass
        elif asset_id=='Asset ID not available ' or asset_id=='':
            pass
        else:
            cursor.execute("""INSERT INTO assets(asset_id,asset_name,tag_uuid,dept_id)values(?,?,?,2)""",asset_id,asset_name,tag_uuid)
    cnxn.commit()


value_insrt()
