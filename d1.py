import pyodbc as py
import time
import smtplib
from pytz import timezone
from datetime import datetime , timedelta
# while True:

server = '10.0.175.122'
database = 'asset'
username = 'SA'
password = 'Soulsvciot01'
cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()
number_of_rows = cursor.execute("SELECT * FROM Activity WHERE reach_time IS NULL")
result= cursor.fetchall()

for row in result:
    ct=datetime.now(timezone("Asia/Kolkata")).strftime("%H:%M:%S.f")
    movement_time=row[9]
    mt=datetime.strptime(movement_time,"%Y-%m-%d %H:%M:%S.%f")
    reach_time=row[10]
    print(mt)
