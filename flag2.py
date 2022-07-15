import pyodbc as py
import string
import csv

db_servername='10.0.2.19'
db_database='asset'
db_username='soul_admin'
db_password='Soulams.svciot'

cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
flag=0
csv_path='/home/u_admin/sap444.csv'
#department=int(input())
#dept_name=input()
#admin=int(input())
list3=[]


#with open("/home/u_admin/sap444.csv",'r',encoding="utf-8") as file:
    #reader = csv.reader(file)
    #header=next(reader)
    #for row in reader:
        #list2.append(row)

   # asset_id=list2[0][2]
    #location=list2[0][12]
    #emp_no=list2[0][16]

def insert_tag():
    cursor=cnxn.cursor()
    #cursor.execute("""INSERT INTO test(asset_id,asset_name,tag_id,asset_price)select asset_id,asset_name,tag_id,asset_price from assets""")
    cursor.execute("""SELECT asset_id,count(asset_id) as count FROM assets group by asset_id having count(asset_id)>1""")
    j=cursor.fetchall()
    for val in j:
        asset_id=val[0]
        count=val[1]
        print(asset_id)
        print(count)
        cursor.execute("""select asset_price,asset_name,location_id from assets where asset_id=(?) and asset_price is not null""",asset_id)
        val=cursor.fetchall()
        for i in val:
            asset_price=i[0]
            asset_name=i[1]
            location_id=i[2]
            if asset_price==None or asset_name==None:
                pass
            else:
                cursor.execute("""UPDATE assets SET asset_price=(?),asset_name=(?),location_id=(?) where asset_id=(?)""",asset_price,asset_name,location_id,asset_id)
        cursor.execute("""DELETE FROM assets where asset_id=(?) and tag_id IS NULL and asset_price IS NOT NULL""",asset_id)
    cnxn.commit()


def change_value():
    cursor = cnxn.cursor()
    cursor.execute("""SELECT asset_id,count(asset_id) as count FROM assets group by asset_id having count(asset_id)>1""")
    i = cursor.fetchall()
    for val in i:
        asset_id=val[0]
        count=val[1]
        cursor.execute("""SELECT asset_name,tag_id from test where asset_id=(?)""", asset_id)
        j = cursor.fetchall()
        for val1 in j:
            name = val1[0]
            tag_id=val1[1]
            print(name)
            print(tag_id)
            if tag_id==None:
               pass
            else:
                cursor.execute("""SELECT tag_uuid from tags where tag_id=(?)""",tag_id)
                k=cursor.fetchall()
                print(k)
                for val2 in k:
                    tag_uuid=val2[0]
                cursor.execute("""UPDATE test SET asset_name=(?) where asset_id=(?) and tag_id=(?)""",name+"-"+str(tag_uuid),asset_id,tag_id)
    cnxn.commit()



def exist_check():
    cursor=cnxn.cursor()
    cursor.execute("""SELECT * from [asset].[dbo].[Untitled 1] """)
    i=cursor.fetchall()
    for rows in i:
        value=i[0]
        value1=value[16]
        cursor.execute("""SELECT count(*) from Employees where emp_no=(?) and dept_name=(?)""",value1,dept_name)
        j=cursor.fetchone()
        emp=j[0]
        if(emp>0):
            print("non-matching employee in",rows)
    cnxn.commit()



def null_check():
    cursor=cnxn.cursor()
    cursor.execute("""SELECT count(*) from [asset].[dbo].[Untitled 1]  where Location IS NULL or Location='0' """)
    i = cursor.fetchone()
    value =i[0]
    print(value)
    cursor.execute("""SELECT count(*) from  [asset].[dbo].[Untitled 1] where Employee_ID IS NULL or Employee_ID='0' """)
    j= cursor.fetchone()
    value1 =j[0]
    print(value1)
    if (value>0):
        flag=1
        print("null location found")
        cursor.execute("""UPDATE [asset].[dbo].[Untitled 1] SET Location=(?) where Location IS NULL or Location='0' """,department)
    elif (value1>0):
        count=1
        print("null employee found")
        cursor.execute("""UPDATE [asset].[dbo].[Untitled 1] SET Employee_ID=(?) where Employee_ID IS NULL or Employee_ID='0' """, admin)
    cnxn.commit()



#file_check()
#value_insrt()
#exist_check()
#null_check()
#insert_tag()
change_value()







