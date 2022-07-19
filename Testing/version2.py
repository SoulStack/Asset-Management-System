import codecs
import logging
from time import sleep
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyodbc as py
import time
from datetime import date
import datetime
import requests
import paho.mqtt.client as mqtt
from rfid_reader import RFIDReader               #used to retrieve system information
from pytz import timezone
import string 
import subprocess as sp#all time zones are available in this modu
import json


logger = logging.getLogger("Status")
logging.basicConfig(filename="Asset.log", filemode='a',format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG )

class Reader:
    """docstring for Reader"""

    def __init__(self, host, port, mqtt_ip, reader_id, db_servername, db_username, db_password, db_database,location_id, cnxn=0, client=0,reader = 0):
        self.host = host
        self.port = port
        # self.db2_servername = db2_servername
        self.db_username = db_username
        self.db_database = db_database
        self.db_password = db_password
        self.db_servername = db_servername
        self.mqtt_ip = mqtt_ip
        self.reader_id = reader_id
        self.cnxn = cnxn
        self.client = client
        self.location_id = location_id
        self.reader = RFIDReader('socket', host=self.host, port=self.port, addr="00")

        # -----------------------------------------------------------
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code" + str(rc))

        # client.subscribe("topic")
        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        # self.client.connect(self.mqtt_ip, 1887,65535)
        #connecting to the mqtt client starting of the program

        while True :
            sleep(1)
            try :
                self.client.connect(self.mqtt_ip, 1887,65535)
                logger.info("mqtt client connected at time {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                break
            except :
                #code for connecting the secondary mqtt server
                print("connecting to secondary mqtt")
                #break

        #Connect to the reader starting of the program

        while True :
            sleep(1)
            try :
                self.reader.connect()
                print("reader is now connected")
                self.client.publish(str(self.reader_id) + "/reader_status", "Connected", qos=1, retain=False)
                break
            except :
                print("reader is disconneted")
                self.client.publish(str(self.reader_id) + "/reader_status", "DisConnected", qos=1, retain=False)

        # trying to connect to the database in the staring of the program.

        while True :
            sleep(1)
            #code changed 18/7/2022
            try :

                self.cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
                print(self.cnxn)
                # if self.cnxn :
                #     self.client.publish( str(self.reader_id) + "/status", "Primary Database is Active", qos=1, retain=False)
                #     print("Primary database is connected") #publishing mqtt about database status
                # else :
                #     self.client.publish( str(self.reader_id) + "/status", "Primary Database is NOtActive", qos=1, retain=False) #publishing

                cursor=self.cnxn.cursor()
                cursor.execute("""SELECT TOP 1 asset_id FROM assets ORDER BY NEWID()""") #checking db is working properly or not
                value = cursor.fetchone()
                if value == None :
                    print("primary Database is Not Active")
                    self.client.publish(str(self.reader_id) + "/status", "Primary Database is Not Active", qos=1, retain=False)

                else :
                    print(value)
                    print("connected to primary database")
                    self.client.publish( str(self.reader_id) + "/status", "Primary Database is Active", qos=1, retain=False) #publishing mqtt about database status
                    logger.info("Connected to the PRIMARY DATABASE at {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                break
            except :
                #try to connect the backup database

                # self.cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db2_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
                # cursor=self.cnxn.cursor()
                # cursor.execute("""SELECT TOP 1 asset_id FROM assets ORDER BY NEWID()""") #checking whether secondary is working or not
                # value = cursor.fetchone()
                # if value == None :
                #     print("Secondary database is Not Active")
                #     self.client.publish("db2_status", "Secondary Database is Not Active", qos=1, retain=False)

                # else :
                #     print(value)
                #     print("connected to secondary database")
                #     logger.info("Connected to the SECONDARY DATABASE at {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                #     self.client.publish("db2_status", "Secondary Database is Active", qos=1, retain=False)
                # sleep(2)


                print(" Primay database not connected")

                #break
            
            #code changed end at 18/07/2022

        #logger.info("#################################################################################################___New Reader Log___######################################################################################")
        logger.info("connected to reader {} @ {}".format(self.reader_id,date.today()))
        logger.info("Scanning started for reader {} at {}".format(self.reader_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))


    #connecting to reader and database (code changed on 18/7/2022)
                             
    #def ping_database(self) :



        #scan tag
    def scan_tag_capture(self):
        #code changing started for scanning of tags
        try:
            self.reader.connect()
            scanned_tags = self.reader.scantags()
            print(scanned_tags)
            if scanned_tags == None :

                pass
            else :

                tags = list(set(scanned_tags))
                return tags
        except Exception as e:
            print("something's wrong with %s:%d. Exception is %s" % (self.host, self.port, e))
            sleep(3)

            #code changed 18/7/2022

            self.client.publish(str(self.reader_id) + "/reader_status", "DisConnected", qos=1, retain=False)
            try:
                self.reader = RFIDReader('socket', host=self.host, port=self.port, addr="00")
                self.reader.connect()
                status,result=sp.getstatusoutput("ping -c1 -w2 " + str(self.host)) #checking reader status each time
                if status==0 :
                    print("Reader is Connected")
                    self.client.publish(str(self.reader_id) + "/reader_status", "Connected", qos=1, retain=False)

                    pass
                else  :
                    self.client.publish(str(self.reader_id) + "/reader_status", "DisConnected", qos=1, retain=False)
                    print("Disconnected")
            except:
                print("Not connected")
                self.client.publish(str(self.reader_id) + "/reader_status", "Check Power Connection of Reader", qos=1, retain=False)
                
            #code change ends 18/7/2022

        #Conversion of bits to string

    def hex_to_string(self, value):
        if value == None:
            pass
        else:

            binary_string = codecs.decode(value,"hex")

            logging.info("tags scanned successfully at reader {} @ {} ".format(self.reader_id,
            datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            return binary_string

    #code changing ends

    #check tag id


    def check_tag_id(self, tag_uuid):
        cursor = self.cnxn.cursor()
        logging.info("tag {} VALIDATION STARTED scanned from READER {}  at {}".format(tag_uuid,self.reader_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
        cursor.execute("""SELECT tag_id  FROM tags where tag_uuid=(?)""", tag_uuid)
        logging.info("tag {} in VALIDATION ENDS scanned from READER {}  @ {}...".format(tag_uuid,self.reader_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
        row = cursor.fetchone()
        if row == None :
            pass
        else :

            return row[0]


    #check tag location


    def check_tag_location(self,tag_id):
        cursor = self.cnxn.cursor()
        # cursor.execute("""SELECT rooms.room_name from rooms INNER JOIN assets ON assets.room_name=rooms.room_name where tag_id=(?)""",(tag_id))                               #not required
        cursor.execute("""SELECT location.location_id from location INNER JOIN assets ON assets.location_id = location.location_id where tag_id =(?)""",(tag_id))
        row = cursor.fetchone()
        if row == None :
            pass
        else :
            return row[0]


    #check whether the tag is in activity or not

    def check_tag_in_activity(self,tag_id):
        cursor = self.cnxn.cursor()
        logging.info("Checking of tag {} in ACTIVITY started at  , time @ {}".format(tag_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
        cursor.execute("""SELECT tag_id FROM Activity WHERE tag_id =(?)""",tag_id)
        logging.info("Checking of tag {}  in ACTIVITY Completed at  , time @ {}".format(tag_id, datetime.datetime.now(
            timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
        row = cursor.fetchone()
        if row == None :
            return 1
        else :
            return row[0]


    #Check approval status from activity :

    def check_approve_status(self, tag_id):
        cursor = self.cnxn.cursor()
        if tag_id == None:
            pass
        else:

            #Code change starts
            logging.info("APPROVAL STATUS checking STARTED for  tag {} at READER {}  @ {}".format(tag_id,self.reader_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            cursor.execute("""SELECT Activity.approve_status FROM Activity WHERE tag_id=(?) """,tag_id)
            row = cursor.fetchone()
            logging.info("APPROVAL STATUS CHECKED  for  tag {} at READER {}  @ {}".format(tag_id, self.reader_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            if row == None:
                returnValue = "Not approved"
            else :
                returnValue = row[0]


            # logger.info("approval status checked for tag {} at reader {} @ {}".format(tag_id,self.reader_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            return returnValue


    #insert into log table

    def insert_into_Log(self, value, tag):
        if tag == None:
            pass
        else:
            cursor = self.cnxn.cursor()
            date = datetime.date.today()
            t = datetime.datetime.now(timezone("Asia/Kolkata"))
            current_time = t.strftime("%H:%M:%S")
            approve = value
            reader = self.reader_id
            tag_id = tag
            cursor.execute("""INSERT INTO Logs(tag_uuid,reader_id,date,time,approve_status)values(?,?,?,?,?) """,
                           (tag_id, reader, date, current_time, approve))
            logger.info("Inserted info of tag {} in Logs table @ {}".format(tag_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
            self.cnxn.commit()


    #change movement status


    def change_movement_status(self, tag, approve_status):
        if tag == None:
            pass
        else:
            cursor = self.cnxn.cursor()
            cursor.execute("""SELECT Activity.starting_point from Activity  WHERE tag_id=(?)""",tag)  # check from the history as per the tag_uuid
            row1 = cursor.fetchone()
            starting_point = row1[0]
            print("staring point is :",starting_point)


            if approve_status == "Approved" and starting_point == self.location_id:
                print("change movement status is executing")
                cursor = self.cnxn.cursor()
                logging.info("Updation of MOVEMENT STATUS in Activity table for tag {} STARTED at time {} ".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                #code changed......
                cursor.execute("""UPDATE Activity SET movement_status=(?),movement_time = (?) WHERE starting_point = (?) and tag_id = (?) """,("moving",datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S"), starting_point,tag))
                logging.info( "Updation of MOVEMENT STATUS and MOVEMENT TIME for tag {} ENDED at time {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                # cursor.execute("""UPDATE Activity SET movement_time = (?) WHERE starting_point = (?) and tag_id =(?)""",(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S"),starting_point,tag))
                self.cnxn.commit()
                #logger.info("Updated movement status in Activity table for tag {} while passing through location {} time @ {}".format(tag,starting_point,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            else:
                #print("else block of movement status is running")
                pass

    #Check destination and starting point

    def check_tag_destination(self, tag_id, approve_status_data):
        tag = tag_id

        approve = approve_status_data
        if tag == None or set():

            pass
        else:
            cursor = self.cnxn.cursor()  # movement status of that particular tag_id
            #code change started...

            cursor.execute("""SELECT Activity.movement_status as movement_status, Activity.destination as destination from Activity WHERE tag_id=(?)""",tag)  # check movement_status  the tag_uuid's movement status\
            row = cursor.fetchone()
            move = row.movement_status
            print("movement status.....",move)
            logging.info("DESTINATION checking STARTED for tag {} at time {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            #cursor.execute("""SELECT Activity.destination from Activity WHERE tag_id=(?)""",tag)  # check destination from the Activity as per the tag_uuid
            #row1 = cursor.fetchone()
            destination = row.destination
            logging.info("DESTINATION checking ENDS for tag {} at time {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""",destination)
            row2 = cursor.fetchone()
            destination_name = row2[0]
            print("destination.......", destination)
            cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""",self.location_id)
            row3 = cursor.fetchone()
            reader_location_name = row3[0]
            print("reader location",reader_location_name)
            #print(type(destination))
            logger.info("Destination of tag {} is {}".format(tag,destination))

            if approve_status_data == "Approved" and move == "moving" :
                if self.location_id==destination :
                    cursor = self.cnxn.cursor()
                    print("executing if block")


                    # cursor.execute("""UPDATE Activity SET Activity.movement_status=(?)  WHERE Activity.destination=(?) and tag_id=(?) """, ("reached",destination,tag))
                    # cursor.execute("""UPDATE Activity SET Activity.approve_status=(?)  WHERE Activity.destination=(?) and tag_id=(?)""", ("Not approved",destination,tag))

                    #code changed
                    cursor.execute("""UPDATE Activity SET Activity.movement_status =(?),Activity.approve_status=(?),Activity.reach_time = (?)  WHERE Activity.destination = (?) and tag_id = (?)""",("reached","Not approved",datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S"), destination,tag))

                    cursor.execute("""UPDATE assets SET location_id=(?) from assets INNER JOIN tags On tags.tag_id=assets.tag_id WHERE tags.tag_id=(?)""",(self.location_id,tag_id))
                    # cursor.execute("""UPDATE assets SET room_id=(?) from assets INNER JOIN tags ON tags.tag_id=assets.tag_id where tags.tag_id=(?)""",(room_id,tag_id))
                    cursor.execute("""insert into History(approve_date,approve_time,emp_id,starting_point,destination,tag_id,movement_status,movement_time,reach_time) SELECT approve_date,approve_time,emp_id,starting_point,destination,tag_id,movement_status,movement_time,reach_time from Activity where tag_id=(?)""",tag)

                    cursor.execute("""delete from Activity where tag_id=(?)""",tag)
                    self.cnxn.commit()  # update the movement status as reached
                    # self.client.connect(self.mqtt_ip, 1887, 60)
                    self.client.publish(str(self.reader_id) + "/status", "Destination : {} Reached".format(destination_name),qos=1 ,retain=False)
                    logger.info("UPDATED APPROVE STATUS and MOVEMENT STATUS in Activity table for tag {} @ {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                    logger.info("Process COMPLETED for tag {} and reached at {} @ time {}".format(tag_id,destination_name,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                else :
                    logging.info("STARTING POINT checking  STARTED  for tag {} at time ".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                    cursor.execute("""SELECT starting_point FROM Activity WHERE tag_id =(?)""",(tag))
                    row = cursor.fetchone()
                    starting_point = row[0]
                    logging.info("STARTING POINT checking ENDS for tag {} at time {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                    if starting_point == self.location_id:
                        self.client.publish(str(self.reader_id) + "/status", "Authorized",qos=1,retain=False)
                        logging.info("The tag {} PASSED ENTRY POINT {} at time {}".format(tag,starting_point,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                        # self.client.loop()
                    else :
                        # EMAIL_SUBJECT = "ALERT:"
                        # co_msg = "the asset of tag {} is Entering to Wrong Location{}".format(tag, reader_location_name)
                        # msg = MIMEText(co_msg)
                        # msg['Subject'] = EMAIL_SUBJECT
                        # mailserver = smtplib.SMTP('smtp.office365.com', 587)
                        # mailserver.ehlo()
                        # mailserver.starttls()
                        # mailserver.login('soul_asset01@outlook.com', 'soulsvciot02')
                        # # Adding a newline before the body text fixes the missing message body
                        #
                        # mailserver.sendmail('soul_asset01@outlook.com', 'soul_asset01@outlook.com', msg.as_string())
                        # mailserver.quit()
                        # self.client.connect(self.mqtt_ip, 1887, 60)
                        logging.info("Mqtt sending started for wrong destination for tag {} at time {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                        self.client.publish(str(self.reader_id) + "/status", "Wrong Destination",qos=1,retain=False)
                        logging.info("mqtt of Wrong destination sent for tag {} at time {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))


            else :

                print("existing to a location....",reader_location_name)
                alert = "Alert On"
                reader_id = self.reader_id
                location_id =self.location_id
                date = datetime.date.today()
                now = datetime.datetime.now(timezone("Asia/Kolkata"))
                time = now.strftime("%H:%M:%S")
                cursor.execute("""INSERT INTO Alert(reader_id,tag_id,location_name,alert_status,alert,date,time,alert_desc,location_id)values(?,?,?,?,?,?,?,?,?) """,
                               (reader_id,tag,reader_location_name, "Normal",alert,date,time,"Wrong Destination",self.location_id))

                # self.client.connect(self.mqtt_ip, 1887,60)
                logging.info("Mqtt for UNAUTHORIZED MOVEMENT sending STARTED for tag {} from location {} at time {}".format(tag,self.location_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                self.client.publish(str(self.reader_id) + "/status","Unauthorized",qos=1,retain=False)
                logging.info("Mqtt SENT Successfully for Unauthorized movement of tag {} from location {} at time {}".format(tag,self.location_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                # self.client.loop()
                self.cnxn.commit()




    #Insert into alert

    def insert_into_alert(self,tag_id):
        cursor = self.cnxn.cursor()
        reader_id = self.reader_id
        alert = "Alert"
        cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""", self.location_id)
        row1 = cursor.fetchone()
        location_name = row1[0]
        alert = "Alert On"
        reader_id = self.reader_id

        date = datetime.date.today()
        now = datetime.datetime.now(timezone("Asia/Kolkata"))
        time = now.strftime("%H:%M:%S")
        cursor.execute("""INSERT INTO Alert(reader_id,tag_id,location_name,alert_status,alert,date,time,alert_desc,location_id)values(?,?,?,?,?,?,?,?,?) """,
            (reader_id, tag_id, location_name, "High", alert, date, time, "Unauthorized Movement",self.location_id))
        self.cnxn.commit()


    def send_mqtt_for_buzzer(self,tag_id,approve_status):
        if tag_id == None :
            pass
        else :
            if approve_status == "Not approved" :
                logging.info("Mqtt sending STARTED for UNAUTHORIZED MOVEMENT of tag {} from {} at time {}".format(tag_id,self.location_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
                self.client.publish(str(self.reader_id) + "/status", "Unauthorized", qos=1, retain=False)
                logging.info("Mqtt SENT Successfully for UNAUTHORIZED MOVEMENT of tag {} from {} at time {}".format(tag_id,self.location_id,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S.%f")))
            else :
                pass


    #tag_alert mail

    # def tag_alert_email(self,tag,approve_status):
    #     if tag == None :
    #         pass
    #     else :
    #         if approve_status == "Not approved":
    #             cursor = self.cnxn.cursor()
    #             cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""", self.location_id)
    #             row3 = cursor.fetchone()
    #             reader_location_name = row3[0]
    #
    #             mailserver = smtplib.SMTP('smtp.office365.com', 587)
    #             mailserver.ehlo()
    #             mailserver.starttls()
    #             mailserver.login('soul_asset01@outlook.com', 'soulsvciot02')
    #             # Adding a newline before the body text fixes the missing message body
    #             mailserver.sendmail('soul_asset01@outlook.com', 'alertasset9@gmail.com', '\nThe asset of tag {} is Unauthorized to move and moving from {}'.format(tag,reader_location_name))
    #             mailserver.quit()
    #
    #
    #         else :
    #             pass
    
    def send_mqtt_to_display(self,data) :
        print(type(data))
        res = not bool(data)
        if res == True :
            pass
        else :

            msg = json.dumps(data)
            self.client.publish(str(self.reader_id) + "/status",payload=msg,qos=1,retain=False)
