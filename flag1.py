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
department=int(input())
dept_name=input()
admin=input()




def file_check():
    try:
        fh=open("/home/u_admin/Untitled 1.csv",'r')
    except IOError:
        print("Error: can't find file or read data")
    else:
        print("File readable")


with open("/home/u_admin/Untitled 1.csv",'r',encoding="utf-8") as file:
    reader = csv.reader(file)
    header=next(reader)
    for row in reader:
        list2.append(row)

    asset_id=list2[0][1]
    location=list2[0][12]
    emp_no=list2[0][17]

def value_insrt():
    for i in range(0,len(list2)):
        cursor=cnxn.cursor()
        cursor.execute("""INSERT INTO test(SAP_Asset_ID_,Location,Employee_ID,sap_loc)values(?,?,?,?)""",asset_id,'7511013',emp_no,location)
    cnxn.commit()


def exist_check():
    cursor=cnxn.cursor()
    cursor.execute("""SELECT * from test """)
    i=cursor.fetchall()
    for rows in i:
        value=i[0]
        value1=value[16]
        cursor.execute("""SELECT count(*) from Employees where emp_no=(?) and dept_work=(?)""",value1,dept_name)
        j=cursor.fetchone()
        emp=j[0]
        if(emp==0):
            print("non-matching employee in",rows)
    cnxn.commit()



def null_check():
    cursor=cnxn.cursor()
    cursor.execute("""SELECT count(*) from test  where sap_loc IS NULL or sap_loc='0' """)
    i = cursor.fetchone()
    value =i[0]
    print(value)
    cursor.execute("""SELECT count(*) from  test  where Employee_ID IS NULL or Employee_ID='0' """)
    j= cursor.fetchone()
    value1 =j[0]
    print(value1)
    if (value>0):
        flag=1
        print("null location found")
        cursor.execute("""UPDATE test SET flag=(?) where sap_loc IS NULL or sap_loc='0' """,flag)
    elif (value1>0):
        count=1
        print("null employee found")
        cursor.execute("""UPDATE test SET Employee_ID=(?),emp_flag=(?) where Employee_ID IS NULL or Employee_ID='0' """, admin,count)
    cnxn.commit()



file_check()
value_insrt()
exist_check()
null_check()

