import pyodbc as py
import time
import smtplib
from pytz import timezone
from datetime import datetime , timedelta
# while True:

server = '10.0.169.136'
database = 'asset'
username = 'SA'
password = 'Soulsvciot01'
cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()
number_of_rows = cursor.execute("SELECT * FROM Activity WHERE reach_time IS NULL")
result= cursor.fetchall()

for row in result :
        move = row[10]
        movement_time  = move[12:19]
        mt =  datetime.strptime(movement_time,"%H:%M:%S")
        expected_time = mt + timedelta(2)
                                                                                        # time_1 = datetime.strptime('05:00:00', "%H:%M:%S")
        ct=datetime.now(timezone("Asia/Kolkata")).strftime("%H:%M:%S")                                                                                # time_2 = datetime.strptime('10:00:00', "%H:%M:%S")

        print(ct)
                                                                                        # time_interval = time_2 - time_1
                                                                                        # print(time_difference)
        reach = row[11]
        print(type(reach))
        reached_time = reach[12:19]
        rt = datetime.strptime(reach_time, "%H:%M:%S")




        if reach == "NULL":
                reach = row[11]
                reached_time = reach[12:19]
                rt = datetime.strptime(reach_time, "%H:%M:%S")

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("assetmanagement.soul@gmail.com", "Soulsvciot01")
                server.sendmail(
                        "assetmanagement.soul@gmail.com",
                        "assetmanagement.soul@gmail.com",
                        "this message is from python")
                server.quit()


# print(r)
cnxn.commit()
# print("Data Detected")
# time.sleep(7200)

