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
import string #all time zones are available in this modu


logger = logging.getLogger("Status")
logging.basicConfig(filename="Asset.log", filemode='a',format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG )

class Reader:
    """docstring for Reader"""

    def __init__(self, host, port, mqtt_ip, reader_id, db_servername, db_username, db_password, db_database,location_id, cnxn=0, client=0,reader = 0):
        self.host = host
        self.port = port
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

        try :

            self.reader.connect()
            print("reader is now connected")
        except :
            print("something went wrong..........")
            sleep(10)
            print("trying to reconnect...........")
            sleep(10)
            try :
                print("try block is executing for connection")
                self.reader.connect()
                print("failed to reconnect")
            except :
                print("reader is power off.....")


        # ------------------------------------------------------------
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code" + str(rc))

        # client.subscribe("topic")
        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.mqtt_ip, 1887,60)
        # self.client.loop_forever()
        self.cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
        logger.info("#################################################################################################___New Reader Log___######################################################################################")
        logger.info("connected to reader {} @ {}".format(self.reader_id,date.today()))
        logger.info("Scanning started at {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
# -------------------------------------------------------------
    #scanning tag
    def scan_tag_capture(self):
        try :
            data = []
            # reader = RFIDReader('socket', host=self.host, port=self.port, addr="00")
            self.reader.connect()
            info = self.reader.getInfo()
            tags = self.reader.scantags()
            # logger.info("Scanning Started at {}".format(datetime.datetime.now(timezone("Asia/Kolkata"))))
            # reader.disconnect()
            return [set(tags)]
        except Exception as e :
            print("Oops!..... Something occurred.")
            print("something's wrong with %s:%d. Exception is %s" % (self.host, self.port, e))
            sleep(10)
            print("trying to reconnect........")
            sleep(10)
            try:
                self.reader = RFIDReader('socket', host=self.host, port=self.port, addr="00")
                self.reader.connect()
            except:
                pass

    # ----------------------------------------------------------
    #conversion of bits to string
    def hex_to_string(self, value):
        if value[0] == set():
            pass
        else:

            filter1 = value[0]
            ss = str(filter1)
            cc = ss[2:-2]
            print(cc)
            if (all(c in string.hexdigits for c in cc) == True) :

            # print(cc)

                b = bytes.fromhex(cc)
                logging.info("tags are converted to string @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                return b.decode()
            else :
                pass
    #-------------------------------------------------------------------------
    #checking the tag is present in tag table or not and finding tag_id
    def check_tag_id(self, tag_uuid):
        cursor = self.cnxn.cursor()
        cursor.execute("""SELECT tag_id  FROM tags where tag_uuid=(?)""", tag_uuid)

        row = cursor.fetchone()
        if row == None :
            pass
        else :

            return row[0]


    #________________________________________________________________________
    #Check tag Tag Location

    def check_tag_location(self,tag_id):
        cursor = self.cnxn.cursor()
        # cursor.execute("""SELECT rooms.room_name from rooms INNER JOIN assets ON assets.room_name=rooms.room_name where tag_id=(?)""",(tag_id))                               #not required
        cursor.execute("""SELECT location.location_id from location INNER JOIN assets ON assets.location_id = location.location_id where tag_id =(?)""",(tag_id))
        row = cursor.fetchone()
        if row == None :
            pass
        else :
            return row[0]
    #_________________________________________________________________________
    #checking tag is present in the activity table or Not

    def check_tag_in_activity(self,tag_id):
        cursor = self.cnxn.cursor()
        cursor.execute("""SELECT tag_id FROM Activity WHERE tag_id =(?)""",tag_id)
        row = cursor.fetchone()
        if row == None :
            return 1
        else :
            return row[0]

    # ----------------------------------------------------------
    #Checking the approval Status Of the Tag

    def check_approve_status(self, tag_id):
        cursor = self.cnxn.cursor()
        if tag_id == None:
            pass
        else:

            #Code change starts
            cursor.execute("""SELECT Activity.approve_status FROM Activity WHERE tag_id=(?) """,tag_id)
            row = cursor.fetchone()
            if row == None:
                returnValue = "Not approved"
            else :
                returnValue = row[0]


            logger.info("approval status checked @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
            return returnValue
            #Code change ends

    # -------------------------------------------------------------
    #Sending Approval_status MQTT

    def approval_status_mqtt(self, approve_data):
        if approve_data == None :
            pass
        else :
            self.client.connect(self.mqtt_ip, 1887)

            logger.info("connected to mqtt server for sending approval @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
            self.client.publish(str(self.reader_id) + "/status", approve_data,qos=2)
            self.client.loop()
            print("mqtt sent")

    # ----------------------------------------------------------------
    #Inserting into LOG table

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


    # ----------------------------------------------------------------
    #Checking tag destination and modification of location
    def check_tag_destination(self, tag_id, approve_status_data):
        tag = tag_id

        approve = approve_status_data
        if tag == None or set():

            pass
        else:
            cursor = self.cnxn.cursor()  # movement status of that particular tag_id
            cursor.execute("""SELECT Activity.movement_status from Activity WHERE tag_id=(?)""",tag)  # check movement_status  the tag_uuid's movement status\
            row = cursor.fetchone()
            move = row[0]
            print("movement status.....",move)
            cursor.execute("""SELECT Activity.destination from Activity WHERE tag_id=(?)""",tag)  # check destination from the Activity as per the tag_uuid
            row1 = cursor.fetchone()
            destination = row1[0]
            # cursor.execute("""SELECT room_id from rooms WHERE room_name = (?)""",destination)#finding room id
            # row2 = cursor.fetchone()
            # room_id = row2[0]
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
                    # cursor.execute("""SELECT location.location_id from location INNER JOIN rooms ON rooms.location_id=location.location_id INNER JOIN reader ON reader.room_name=rooms.room_name where reader_id=(?)""",self.reader_id)
                    # row1 = cursor.fetchone()
                    # location_id = row1[0]


                    cursor.execute("""UPDATE Activity SET Activity.movement_status=(?)  WHERE Activity.destination=(?) and tag_id=(?) """, ("reached",destination,tag))
                    cursor.execute("""UPDATE Activity SET Activity.approve_status=(?)  WHERE Activity.destination=(?) and tag_id=(?)""", ("Not approved",destination,tag))
                    cursor.execute("""UPDATE Activity SET Activity.reach_time = (?)  WHERE Activity.destination = (?) and tag_id = (?)""",(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S"), destination,tag))
                    #cursor.execute("""UPDATE Activity SET starting_point= (?) WHERE tag_id= (?)""",(destination,tag))
                    #cursor.execute("""UPDATE Activity SET destination= NULL WHERE tag_id= (?)""",(tag))
                    #location and location name updation for particular tag_id
                    # cursor.execute("""UPDATE assets SET room_name=(?) FROM assets where tag_id=(?)""",(destination,tag))
                    #update location id in asset
                    cursor.execute("""UPDATE assets SET location_id=(?) from assets INNER JOIN tags On tags.tag_id=assets.tag_id WHERE tags.tag_id=(?)""",(self.location_id,tag_id))
                    # cursor.execute("""UPDATE assets SET room_id=(?) from assets INNER JOIN tags ON tags.tag_id=assets.tag_id where tags.tag_id=(?)""",(room_id,tag_id))
                    cursor.execute("""insert into History(approve_date,approve_time,emp_id,starting_point,destination,tag_id,movement_status,movement_time,reach_time) SELECT approve_date,approve_time,emp_id,starting_point,destination,tag_id,movement_status,movement_time,reach_time from Activity where tag_id=(?)""",tag)

                    cursor.execute("""delete from Activity where tag_id=(?)""",tag)
                    self.cnxn.commit()  # update the movement status as reached
                    self.client.connect(self.mqtt_ip, 1887, 60)

                    self.client.publish(str(self.reader_id) + "/status", "Destination : {} Reached".format(destination))
                    self.client.loop()
                    logger.info("Updated approve status and movement status in Activity table for tag {} @ {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                    logger.info("Process completed @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
                else :
                    cursor.execute("""SELECT starting_point FROM Activity WHERE tag_id =(?)""",(tag))
                    row = cursor.fetchone()
                    starting_point = row[0]
                    if starting_point == self.location_id:
                        self.client.publish(str(self.reader_id) + "/status", "Entry point",qos=2)
                        self.client.loop()

                        pass
                    else :
                        # # EMAIL_FROM = "soul_asset01@outlook.com"
                        # # EMAIL_TO = "alertasset9@gmail.com"
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
                        # mailserver.sendmail('soul_asset01@outlook.com', 'soul_asset01@outlook.com',msg.as_string() )
                        # mailserver.quit()
                        # self.client.connect(self.mqtt_ip, 1883)
                        self.client.connect(self.mqtt_ip, 1887, 60)

                        self.client.publish(str(self.reader_id) + "/status", "Wrong Destination",qos=2)


            else :
                # cursor.execute("""SELECT location_name from location INNER JOIN rooms ON rooms.location_id=location.location_id INNER JOIN reader ON reader.room_name=rooms.room_name where reader_id=(?)""",self.reader_id)

                # row1 = cursor.fetchone()
                # location_name = row1[0]

                print("existing to a location....",reader_location_name)
                alert = "Alert On"
                reader_id = self.reader_id
                location_id =self.location_id
                date = datetime.date.today()
                now = datetime.datetime.now(timezone("Asia/Kolkata"))
                time = now.strftime("%H:%M:%S")
                cursor.execute("""INSERT INTO Alert(reader_id,tag_id,location_name,alert_status,alert,date,time,alert_desc,location_id)values(?,?,?,?,?,?,?,?,?) """,
                               (reader_id,tag,reader_location_name, "Normal",alert,date,time,"Wrong Destination",self.location_id))

                self.client.connect(self.mqtt_ip, 1887,qos=2)

                self.client.publish(str(self.reader_id) + "/status","Not approved",qos=2)
                self.client.loop()
                # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                # server.quit()
                self.cnxn.commit()

    #___________________________________________________
    #Alerting movement of tag

    def tag_alert_email(self,tag,approve_status):
        if tag == None :
            pass
        else :
            if approve_status == "Not approved":
                cursor = self.cnxn.cursor()
                cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""", self.location_id)
                row3 = cursor.fetchone()
                reader_location_name = row3[0]

                # EMAIL_FROM = "soul_asset01@outlook.com"
                # EMAIL_TO = "alertasset9@gmail.com"
                # EMAIL_SUBJECT = "ALERT:"
                # co_msg = "the asset of tag {} is not approved and moving from {}".format(tag, reader_location_name)
                # msg = MIMEText(co_msg)
                # msg['Subject'] = EMAIL_SUBJECT
                # mailserver = smtplib.SMTP('smtp.office365.com', 587)
                # mailserver.ehlo()
                # mailserver.starttls()
                # mailserver.login('soul_asset01@outlook.com', 'soulsvciot02')
                # # Adding a newline before the body text fixes the missing message body
                # mailserver.sendmail('soul_asset01@outlook.com', 'soul_asset01@outlook.com',msg.as_string())
                # mailserver.quit()


            else :
                pass

    #____________________________________________________________
    #Changing movement status of a tag
    def change_movement_status(self, tag, approve_status):
        if tag == None:
            pass
        else:
            cursor = self.cnxn.cursor()
            cursor.execute("""SELECT Activity.starting_point from Activity  WHERE tag_id=(?)""",tag)  # check from the history as per the tag_uuid
            row1 = cursor.fetchone()
            starting_point = row1[0]
            print("staring point is :",starting_point)
            # cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""", self.location_id)
            # row3 = cursor.fetchone()
            # reader_location_name = row3[0]

            if approve_status == "Approved" and starting_point == self.location_id:
                print("change movement status is executing")
                cursor = self.cnxn.cursor()
                cursor.execute("""UPDATE Activity SET movement_status=(?) WHERE starting_point = (?) and tag_id = (?) """,("moving", starting_point,tag))
                cursor.execute("""UPDATE Activity SET movement_time = (?) WHERE starting_point = (?) and tag_id =(?)""",(datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S"),starting_point,tag))
                self.cnxn.commit()
                logger.info("Updated movement status in Activity table for tag {} @ {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata")).strftime("%d/%m/%Y %H:%M:%S")))
            else:
                print("else block of movement status is running")
                pass
    #_________________________________________________________________
    #Finding latest record from log
    #def latest_from_logs(self):
        ##cursor.execute("""SELECT TOP 1 * FROM Logs ORDER BY log_id DESC""")

        ##return (row[1])
    #__________________________________________________________________
    #Send alert if the tag is not in activity and in asset tablke
    def alert_movement(self,tag_id):
        if tag_id== None :
            pass
        else :
            location = self.location_id
            cursor = self.cnxn.cursor()
            cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""", self.location_id)
            row3 = cursor.fetchone()
            location_name = row3[0]

            # # EMAIL_FROM = "soul_asset01@outlook.com"
            # # EMAIL_TO = "alertasset9@gmail.com"
            # EMAIL_SUBJECT = "ALERT:"
            # co_msg = "the asset of tag {} is not authorized to move  and moving from {}".format(tag_id, location_name)
            # msg = MIMEText(co_msg)
            # msg['Subject'] = EMAIL_SUBJECT
            # mailserver = smtplib.SMTP('smtp.office365.com', 587)
            # mailserver.ehlo()
            # mailserver.starttls()
            # mailserver.login('soul_asset01@outlook.com', 'soulsvciot02')
            # # Adding a newline before the body text fixes the missing message body
            # mailserver.sendmail('soul_asset01@outlook.com', 'soul_asset01@outlook.com',msg.as_string())
            # mailserver.quit()
            # self.client.connect(self.mqtt_ip, 1883)
            self.client.connect(self.mqtt_ip, 1887, 60)

            self.client.publish(str(self.reader_id) + "/status", "Unauthorized",qos=2)
            self.client.loop()

    def insert_into_alert(self,tag_id):
        cursor = self.cnxn.cursor()

        # room_name = self.room_name
        reader_id = self.reader_id
        alert = "Alert"

        # cursor.execute("""SELECT location_name from location INNER JOIN rooms ON rooms.location_id=location.location_id INNER JOIN reader ON reader.room_name=rooms.room_name where reader_id=(?)""",self.reader_id)
        cursor.execute("""SELECT location_name FROM location WHERE location_id =(?)""", self.location_id)
        row1 = cursor.fetchone()
        location_name = row1[0]
        alert = "Alert On"
        reader_id = self.reader_id
        # room_name = self.room_name

        date = datetime.date.today()
        now = datetime.datetime.now(timezone("Asia/Kolkata"))
        time = now.strftime("%H:%M:%S")
        # approve = "not approved"
        cursor.execute("""INSERT INTO Alert(reader_id,tag_id,location_name,alert_status,alert,date,time,alert_desc,location_id)values(?,?,?,?,?,?,?,?,?) """,
            (reader_id, tag_id, location_name, "High", alert, date, time, "Unauthorized Movement",self.location_id))
        self.cnxn.commit()

    def send_mqtt_to_display(self,tag_id,approve_status):
        if tag_id == None :
            pass
        else :
            cursor = self.cnxn.cursor()

            cursor.execute("""SELECT Activity.starting_point from Activity  WHERE tag_id=(?)""",
                           tag_id)  # check from the history as per the tag_uuid
            row1 = cursor.fetchone()
            if row1 ==None :
                pass
            else:

                starting_point = row1[0]
                print("staring point is :", starting_point)
                self.client.connect(self.mqtt_ip, 1887)

                if approve_status == "Approved" and starting_point== self.reader_id :
                    self.client.publish(str(self.reader_id)+"/status","Authorized")
                    self.client.loop()
                    print("mqtt sent")
                # elif approve_status == None :
                #     self.client.publish(str(self.reader_id) +"/status", "Unauthorized")
                #     print("mqtt sent")
                else:
                    self.client.publish(str(self.reader_id)+"/status", "Unauthorized")
                    self.client.loop()
                    print("mqtt sent")



