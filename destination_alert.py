import pyodbc as py
import time
from time import sleep
import smtplib
from pytz import timezone
from datetime import datetime , timedelta
# while True:

server = '10.0.175.122'
database = 'asset'
username = 'SA'
password = 'Soulsvciot01'
cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

while True :
        sleep(7200)
        number_of_rows = cursor.execute("SELECT * FROM Activity WHERE reach_time IS NULL ")
        result= cursor.fetchall()
        print(result)


        for row in result :
                move = row[9]
                print(move)
                if move == None :
                        pass
                else :
                        movement_time  = move[11:19]
                        print(movement_time)
                        mt =  datetime.strptime(movement_time,"%H:%M:%S")
                        print("movement time is ",mt.time())
                        expected_time = mt.time() + timedelta(2)
                        print("expected time is ",expected_time)
                        current_time=datetime.now(timezone("Asia/Kolkata")).strftime("%H:%M:%S")
                        print("current time is ",current_time)
                        reach = row[10]
                # print(type(reach))
                # if reach == "None":
                #         pass
                # else :
                #         reached_time = reach[12:19]
                #         rt = datetime.strptime(reached_time, "%H:%M:%S")
                #         print(rt)

                        if reach == "NULL":
                                if current_time > expected_time :



                                        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                        server.login("assetsoul22@gmail.com", "Soulsvciot01")
                                        server.sendmail(
                                                "assetsoul22@gmail.com",
                                                "assetsoul22@gmail.com",
                                                "this message is from python")
                                        server.quit()



                cnxn.commit()

