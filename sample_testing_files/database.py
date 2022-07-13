import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'soulasset.database.windows.net' 
database = 'asset' 
username = 'assetadmin' 
password = 'Soulsvciot01' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#Sample select query
cursor.execute("SELECT * FROM tags") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()
