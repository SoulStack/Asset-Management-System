import pyodbc
server = 'soulasset.database.windows.net'
database = 'asset'
username = 'assetadmin'
password = 'Soulsvciot01'
cnxn = pyodbc.connect('DRIVER={CData ODBC Driver for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("""
SELECT tags.tag_uuid, History.approve_status
FROM tags
INNER JOIN History ON History.tag_id= tags.tag_id
WHERE tag_uuid='SOULRFT000001' """)

row = cursor.fetchone()
print(row[1])
