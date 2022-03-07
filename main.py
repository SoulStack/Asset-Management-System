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
import datetime
class Reader:

		
	"""docstring for Reader"""
	def __init__(self,host,port,mqtt_ip,reader_id,db_servername,db_username,db_password,db_database,cnxn=0):
		self.host = host
		self.port = port
		self.db_username = db_username
		self.db_database = db_database
		self.db_password = db_password
		self.db_servername = db_servername
		self.mqtt_ip =mqtt_ip
		self.reader_id =  reader_id
		self.cnxn = cnxn
		logging.basicConfig(filename=self.reader_id+".log",filemode='w', format='%(name)s - %(levelname)s - %(message)s')
		logging.info('This will get logged to a file')
		self.cnxn = py.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+db_servername+';DATABASE='+db_database+';UID='+db_username+';PWD='+db_password)

		if type(self.reader_id) == str:
			pass
		else:
			print("please enter string type for topic")
			logging.error("error in topic not str"+str(datetime.datetime.now))
			pass
		print("sucess")
		logging.info("connected to reader @ {}".format(date.today()))
	#-------------------------------------------------------------
	def scan_tag_capture(self): #stage 2
		data=[]
		reader = RFIDReader('socket',host=self.host,port=self.port,addr="00")
		reader.connect()
		n=True
		info=reader.getInfo()
		tags=reader.scantags()
		logging.info("tagged scanned "+str(datetime.datetime.now))
		#reader.disconnect()
		return [set(tags)]
	#-------------------------------------------------------------
	def reader_status(self): #stage 1
		host=self.host
		parameter = '-n' if platform.system().lower()=='windows' else '-c'
		command = ['ping',parameter,'1',host]
		response = subprocess.call(command)
		if response ==0:
			return "Connected"
			logging.info(self.reader_id+" connected "+str(datetime.datetime.now))
		else:
			return "disconnected"
			logging.info(self.reader_id+" disconnected "+str(datetime.datetime.now))
	#-------------------------------------------------------------
	def check_approve_status(self,tag_uuid):
		cursor = self.cnxn.cursor()
		cursor.execute("""SELECT tags.tag_uuid, History.approve_status FROM tags INNER JOIN History ON History.tag_id=tags.tag_id WHERE tag_uuid=(?) """,tag_uuid)
		row= cursor.fetchone()
		logging.info("approval status "+str(datetime.datetime.now))
		return (row[1])
	#-------------------------------------------------------------
	def insert_into_activity(self): #stage 3
		
		logging.info("activity log for tags: "+str(datetime.datetime.now))
	#-------------------------------------------------------------
	def reader_status_mqtt(self,data):
		def on_connect(client,userdata,flags,rc):
			print("Connected with result code"+str(rc))
			#client.subscribe("topic")
		def on_message(client,userdata,msg):
			print(msg.topic+" "+str(msg.payload))
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect(self.mqtt_ip, 1883, 60)
		logging.info("connected to mqtt server "+str(datetime.datetime.now))
		client.publish(self.reader_id+"/data",data,qos=0,retain=False)
		logging.info("published data:mqtt/"+data+str(datetime.datetime.now))
		logging.info("mqtt running "+str(datetime.datetime.now))
	def hex_to_string(self,value):
		if value[0]==set():
			pass
		else:
			filter1=value[0]
			ss=str(filter1)
			cc=ss[2:-2]
			print(cc)
			b=bytes.fromhex(cc)
			logging.info("tags are converted to string "+str(datetime.datetime.now))
			return b.decode()
	def approval_status_mqtt(self,approve_data):
		def on_connect(client,userdata,flags,rc):
			print("Connected with result code"+str(rc))
			#client.subscribe("topic")
		def on_message(client,userdata,msg):
			print(msg.topic+" "+str(msg.payload))
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect(self.mqtt_ip, 1883, 60)
		logging.info("connected to mqtt server for sending approval "+str(datetime.datetime.now))
		client.publish(self.reader_id+"/approval_status",approve_data,qos=0,retain=False)
		logging.info("connected to mqtt server for sending approval "+str(datetime.datetime.now))
