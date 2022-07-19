import pyodbc as py
import string
import csv

db_servername='10.0.2.19'
db_database='asset'
db_username='SA'
db_password='Soulsvciot01'

cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
list2=[]

with open("/home/u_admin/EMPLOYEE DETAILS.csv",'r',encoding="utf-8") as file:
    reader = csv.reader(file)
    header=next(reader)
    for row in reader:
        list2.append(row)
    #print(list2)


def emp_master():
    for i in list2:
        emp_id=i[0]
        title = i[1]
        name = i[2]
        pos_id = i[3]
        des = i[4]
        doj = i[5]
        area = i[6]
        org_area = i[7]
        group = i[8]
        dob = i[9]
        per_email = i[10]
        per_email1 = per_email.lower()
        off_email = i[11]
        off_email1 = off_email.lower()
        contact = i[12]
        cursor=cnxn.cursor()
        cursor.execute("""INSERT INTO Employee_master(emp_id,title,emp_name,position_id,designation,date_of_joining,personal_area,original_unit,emp_group,DOB,personal_email,official_email,mobile)values(?,?,?,?,?,?,?,?,?,?,?,?,?)""",emp_id,title,name,pos_id,des,doj,area,org_area,group,dob,per_email1,off_email1,contact)
    cnxn.commit()

def emp_insrt():
    for i in list2:
        emp_id = i[0]
        title = i[1]
        name = i[2]
        pos_id = i[3]
        des = i[4]
        doj = i[5]
        area = i[6]
        org_area = i[7]
        group = i[8]
        dob = i[9]
        per_email = i[10]
        per_email1 = per_email.lower()
        off_email = i[11]
        off_email1 = off_email.lower()
        contact = i[12]
        name1 = name.split(' ')
        first_name = name1[0]
        last_name = name1[1]
        if last_name=='':
            last_name=name1[2]
        if org_area=='School of Mechanical Engineering':
            org_area='MECHANICAL'
        elif org_area=='School of Electronics Engineering':
            org_area='COMMON ELECTRONICS ENGG'
        elif org_area=='ICT Cell':
            org_area='ICT CELL KIIT CORE'

    cursor=cnxn.cursor()
    cursor.execute("""INSERT INTO Employees(emp_no,first_name,last_name,dept_work,contact_no,hire_date,job,ed_level,DOB,emp_title)values(?,?,?,?,?,?,?,?,?,?)""",emp_id,first_name,last_name,org_area,contact,doj,des,group,DOB,title)
    cursor.execute("""INSERT INTO Users(user_id,user_name,email)values(?,?,?)""",emp_id,name,off_email1+"/"+per_email1)
    for i in list2:
        if off_email==None and per_email==None:
        elif off_email=='' and per_email=='':
            cursor.execute("""UPDATE Users SET email=(?) where user_id=(?)""",first_name+"."+last_name+"@kiit.ac.in",emp_id)
    cnxn.commit()





#emp_master()
emp_insrt()









