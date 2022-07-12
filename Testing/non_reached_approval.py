import pyodbc as py
import time
while True:
	print("Starting")
	server = '10.0.175.122'
	database = 'asset'
	username = 'SA'
	password = 'Soulsvciot01'
	cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
	cursor = cnxn.cursor()
	cursor.execute("Select * FROM Activity Where approve_status = 'False' AND movement_status='False'")
	r=cursor.fetchmany()
	print(r)
	cnxn.commit()
	print("Data Detected")
	time.sleep(7200)
