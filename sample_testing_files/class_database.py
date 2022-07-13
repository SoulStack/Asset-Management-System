import pyodbc as py

class Database(object):
        """docstring for Database"""
        def __init__(self,server,username,password,database):
                self.server = server
                self.username = username
                self.password = password
                self.database = database
                print("database initiated")
        def query(self):
                cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
                cursor = cnxn.cursor()
                cursor.execute("""SELECT tags.tag_uuid, History.approve_status FROM tags INNER JOIN History ON History.tag_id=tags.tag_id WHERE tag_uuid='SOULRFT000001' """)
                row = cursor.fetchone()
                print(row[1])

azure_asset = Database("soulasset.database.windows.net","assetadmin","Soulsvciot01","asset")
azure_asset.query()
