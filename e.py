import pyodbc as py
import datetime

server = '10.0.175.122'
database = "asset"
username = 'SA'
password = 'Soulsvciot01'
cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("""INSERT INTO Activity(tag_uuid,reader_id,date,time,approval_status)values('abc','reader1','12','20','false')""")
