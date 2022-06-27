import pyodbc as py
import string
import csv

db_servername='10.0.175.122'
db_database='asset'
db_username='SA'
db_password='Soulsvciot01'

cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)

list2=[]
flag=0
department=2
admin=1007

with open("/home/u_admin/sap444.csv",'r',encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        list2.append(row)
        #print(list2)
    asset_id=list2[1][2]
    location=list2[1][12]
    emp_no=list2[1][16]
    #print(location)
    #print((emp_no))
    #print(location)
    #print(location)
def value_check():
    for i in range(0,len(list2)):
        cursor=cnxn.cursor()
        cursor.execute("""BULK INSERT [asset].[dbo].[Untitled 1] FROM '/home/u_admin/sap444.csv' WITH(FIRSTROW = 2, FIELDTERMINATOR = ',',ROWTERMINATOR='\n',MAXERRORS=1)""")
    cnxn.commit()


def null_check():
    cursor=cnxn.cursor()
    cursor.execute("""SELECT Location from [asset].[dbo].[Untitled 1] where Location=(?)""", location)
    i = cursor.fetchone()
    value = i[0]
    cursor.execute("""SELECT Employee_ID from  [asset].[dbo].[Untitled 1] where Employee_ID=(?)""", emp_no)
    j= cursor.fetchone()
    value1 = j[0]
    if (value == None):
        flag=1
        print("null location")
        cursor.execute("""UPDATE INSERT INTO [asset].[dbo].[Untitled 1] SET Location=(?) where location IS NULL or location=0""",department)
    elif (value1 == None):
        count=1
        print("null employee")
        cursor.execute("""UPDATE [asset].[dbo].[Untitled 1] SET Employee_ID=(?) where emp_no IS NULL lor emp_no=0""", admin)
    cnxn.commit()


null_check()
value_check()






