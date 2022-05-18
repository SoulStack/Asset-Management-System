import pyodbc as py

server = '10.0.175.122'
database = 'asset'
username = 'SA'
password = 'Soulsvciot01'
cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()


def latest_from_logs():
    cursor = cnxn.cursor()
    cursor.execute("""SELECT tag_id FROM tags  where tag_uuid='SA/ele/a6/0001'""")
    

    row = cursor.fetchone()
    if row == None :
        print("this tag is not exists")
    else  :
        print(row[0])


b = latest_from_logs()

