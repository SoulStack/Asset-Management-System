import logging
import pyodbc as py
import time
from datetime import date
import requests
import paho.mqtt.client as mqtt
from rfid_reader import RFIDReader
import json
import platform
import subprocess
import logging
from pytz import timezone
import datetime


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

        logging.basicConfig(filename=str(self.reader_id) + ".log", filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')
        logging.info('This will get logged to a file')
        self.cnxn = py.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_servername + ';DATABASE=' + db_database + ';UID=' + db_username + ';PWD=' + db_password)
        if type(self.reader_id) == str:
            pass
        else:
            print("please enter string type for topic")
            logging.error("error in topic not str" + str(datetime.datetime.now))
            pass
        print("success")
        logging.info("connected to reader @ {}".format(date.today()))

    # -------------------------------------------------------------
    def scan_tag_capture(self):  # stage 2
        data = []
        reader = RFIDReader('socket', host=self.host, port=self.port, addr="00")
        reader.connect()
        n = True
        info = reader.getInfo()
        tags = reader.scantags()
        logging.info("tagged scanned " + str(datetime.datetime.now))
        # reader.disconnect()
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
            logging.info("tags are converted to string " + str(datetime.datetime.now))
            return b.decode()

    # ----------------------------------------------------------
    def check_approve_status(self, tag_uuid):
        cursor = self.cnxn.cursor()
        if tag_uuid == None:
            pass
        else:

            cursor.execute("""SELECT tags.tag_uuid, Activity.approve_status FROM tags INNER JOIN Activity ON Activity.tag_id=tags.tag_id WHERE tag_uuid=(?) """,tag_uuid)
            row = cursor.fetchone()
            logging.info("approval status " + str(datetime.datetime.now))
            return (row[1])

    # -------------------------------------------------------------

    def approval_status_mqtt(self, approve_data):
        logging.info("connected to mqtt server for sending approval " + str(datetime.datetime.now))
        self.client.publish(str(self.reader_id) + "/approval_status", approve_data, qos=0, retain=False)
        logging.info("connected to mqtt server for sending approval " + str(datetime.datetime.now))

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
            logging.info("activity log for tags: " + str(datetime.datetime.now) + " " + str(taguuid))
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

        if approve_status_data == True and move == True and destination == self.location:
            cursor = self.cnxn.cursor()
            cursor.execute("""UPDATE Activity SET movement_status=0 WHERE destination = (?) """,destination)
            cursor.execute("""UPDATE Activity SET approve_status=0 WHERE destination = (?)""",destination)
            self.cnxn.commit()# update the movement status as reached
        else:
            pass
