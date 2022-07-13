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
	cursor.execute("DELETE FROM Alert WHERE approval_status = 'False'")
	cnxn.commit()
	print("Data deleted")
	time.sleep(7200)
