import pymssql
server = 'soulasset.database.windows.net'
database = 'asset'
username = 'assetadmin'
password = 'Soulsvciot01'
cnxn = pymssql.connect(server,username,password,"asset")
cursor = cnxn.cursor()
cursor.execute("""
SELECT tags.tag_uuid, History.approve_status
FROM tags
INNER JOIN History ON History.tag_id= tags.tag_id
WHERE tag_uuid='SOULRFT000001' """)

row = cursor.fetchone()
print(row[1])
