import pyodbc as py
def check_approve_status(tag):
                server = 'soulasset.database.windows.net'
                database = "asset"
                username = 'assetadmin'
                password = 'Soulsvciot01'
                cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
                cursor = cnxn.cursor()
                cursor.execute(""" SELECT tags.tag_uuid, History.approve_status FROM tags INNER JOIN History ON History.tag_id=tags.tag_id WHERE tag_uuid=(?)  """,(tag))
                row= cursor.fetchone()
                return (row[1])
if __name__ == "__main__" :
        tag_uuid = "soul/ast/00004"
        print( check_approve_status(tag_uuid))
