import logging
import pyodbc as py
import time
from datetime import date
import datetime
import requests
import paho.mqtt.client as mqtt
from rfid_reader import RFIDReader
import json
import platform
import logging
from pytz import timezone
import datetime

logger = logging.getLogger("Status")
logging.basicConfig(filename="Asset.log", filemode='a',format='%(name)s - %(levelname)s - %(message)s',level = logging.DEBUG )

class Reader:
    """docstring for Reader"""

    def __init__(self, host, port, mqtt_ip, reader_id, db_servername, db_username, db_password, db_database,location, cnxn=0, client=0):
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
        self.location = location
        # ------------------------------------------------------------
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code" + str(rc))

        # client.subscribe("topic")
        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.mqtt_ip, 1883, 60)
        self.cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
        logger.info("#################################################################################################___New Reader Log___######################################################################################")
        logger.info("connected to reader {} @ {}".format(self.reader_id,date.today()))
        logger.info("Scanning started at {}".format(datetime.datetime.now(timezone("Asia/Kolkata"))))

    # -------------------------------------------------------------
    def scan_tag_capture(self):  # stage 2
        data = []
        reader = RFIDReader('socket', host=self.host, port=self.port, addr="00")
        reader.connect()
        n = True
        tags = reader.scantags()
        return [set(tags)]

    # ----------------------------------------------------------
    def hex_to_string(self, value):
        if value[0] == set():
            pass
        else:
            filter1 = value[0]
            ss = str(filter1)
            cc = ss[2:-2]
            print(cc)
            b = bytes.fromhex(cc)
            logging.info("tags are converted to string @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata"))))
            return b.decode()

    # ----------------------------------------------------------
    def check_approve_status(self, tag_uuid):
        cursor = self.cnxn.cursor()
        if tag_uuid == None:
            pass
        else:

            cursor.execute("""SELECT tags.tag_uuid, Activity.approve_status FROM tags INNER JOIN Activity ON Activity.tag_id=tags.tag_id WHERE tag_uuid=(?) """,tag_uuid)
            row = cursor.fetchone()
            logger.info("approval status checked @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata"))))
            return (row[1])

    # -------------------------------------------------------------

    def approval_status_mqtt(self, approve_data):
        if approve_data == None :
            pass
        else :

            logger.info("connected to mqtt server for sending approval @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata"))))
            self.client.publish(str(self.reader_id) + "/approval_status", approve_data, qos=0, retain=False)

    # ----------------------------------------------------------------
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
            taguuid = tag
            cursor.execute("""INSERT INTO Logs(tag_uuid,reader_id,date,time,approve_status)values(?,?,?,?,?) """,
                           (taguuid, reader, date, current_time, approve))
            logger.info("Inserted info of tag {} in Logs table @ {}".format(taguuid,datetime.datetime.now(timezone("Asia/Kolkata"))))
            self.cnxn.commit()

    # ----------------------------------------------------------------
    def check_tag_destination(self, tag_uuid, approve_status_data):
        tag = tag_uuid

        approve = approve_status_data
        if tag == None or set():

            pass
        else:
            cursor = self.cnxn.cursor()  # movement status of that particular tag_id
            cursor.execute("""SELECT Activity.movement_status from Activity INNER JOIN tags ON tags.tag_id=Activity.tag_id WHERE tag_uuid=(?)""",tag)  # check the tag_id's movement status\
            row = cursor.fetchone()
            move = row[0]
            print(move)
            cursor.execute("""SELECT Activity.destination from Activity INNER JOIN tags ON tags.tag_id=Activity.tag_id WHERE tag_uuid=(?)""",tag)  # check from the history as per the tag_uuid
            row1 = cursor.fetchone()
            destination = row1[0]
            print(destination)
            print(type(destination))
            logger.info("Destination of tag {} is {}".format(destination,tag))

            if approve_status_data == "True" and move == "True" :
                if self.location == destination :
                    cursor = self.cnxn.cursor()
                    print("executing if block")
                    cursor.execute("""UPDATE Activity SET movement_status=(?) WHERE destination = (?) """, ("False",destination))
                    cursor.execute("""UPDATE Activity SET approve_status=(?) WHERE destination = (?)""", ("False",destination))
                    self.cnxn.commit()  # update the movement status as reached
                    logger.info("Updated approve status and movement status in Activity table for tag {} @ {}".format(tag,datetime.datetime.now(timezone("Asia/Kolkata"))))
                    logger.info("Process completed @ {}".format(datetime.datetime.now(timezone("Asia/Kolkata"))))
                else :
                    print("wrong destination")
            else :
                print("Asset is not moving")
                pass


