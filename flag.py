import logging
from time import sleep
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyodbc as py
import time
from datetime import date
import datetime
import requests
import paho.mqtt.client as mqtt
from rfid_reader import RFIDReader               #used to retrieve system information
from pytz import timezone
import string
import csv

db_servername='10.0.175.122'
db_database='asset'
db_username='SA'
db_password='Soulsvciot01'

cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)

def check_flag():
    cursor = cnxn.cursor()
    #cursor.execute("""BULK INSERT [asset].[dbo].[Untitled 1] FROM '/home/u_admin/sap444.csv' WITH(FIRSTROW = 2, FIELDTERMINATOR = ',',ROWTERMINATOR='\n',MAXERRORS=1)""")
    cursor.execute("""SELECT emp_no from assets""")
    row1=cursor.fetchone()
    value=row1[0]

    if value==None or value==0:
        print("executing")
        cursor.execute("""UPDATE assets SET flag=1""")
        cnxn.commit()
    else:
        pass
def bulk_insrt():
    cursor = cnxn.cursor()
    cursor.execute("""EXEC insrt_errors""")
    err=cursor.fetchone()
    value1=err[0]
    if value1>0:
        cursor.execute("""UPDATE [asset].[dbo].[Untitled 1] SET flag=1""")
    cnxn.commit()


#check_flag()
bulk_insrt()





