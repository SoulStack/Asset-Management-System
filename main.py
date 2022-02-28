import logging
import pyodbc
import time
from datetime import date
import requests
import paho.mqtt.client as mqtt
from rfid_reader import RFIDReader
import json
import platform
import subprocess
class Reader:
	"""docstring for Reader"""
	def __init__(self,host,port,mqtt_ip,reader_id):
		self.host = host
		self.port = port
		self.mqtt_ip =mqtt_ip
		self.reader_id =  reader_id
		if type(self.reader_id) == str:
			pass
		else:
			print("please enter string type for topic")
			pass
		print("sucess: please connect")
		logging.info("connected to reader @ {}".format(date.today()))
	#-------------------------------------------------------------
	def scan_tag_capture(self): #stage 2
		data=[]
		reader = RFIDReader('socket',host=self.host,port=self.port,addr="00")
		reader.connect()
		n=True
		info=reader.getInfo()
		tags=reader.scantags()
		reader.disconnect()
		return [set(tags)]
	#-------------------------------------------------------------
	def reader_status(self): #stage 1
		host=self.host
		parameter = '-n' if platform.system().lower()=='windows' else '-c'
		command = ['ping',parameter,'1',host]
		response = subprocess.call(command)
		if response ==0:
			return "Connected"
		else:
			return "disconnected"
	#-------------------------------------------------------------
	def check_approve_status(self): 
		pass
		#this is for database code
	#-------------------------------------------------------------
	def insert_into_activity(self): #stage 3
		pass
		#this is for database code
	#-------------------------------------------------------------
	def send_data_via_mqtt(self,data):
		def on_connect(client,userdata,flags,rc):
			print("Connected with result code"+str(rc))
			#client.subscribe("topic")
		def on_message(client,userdata,msg):
			print(msg.topic+" "+str(msg.payload))
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect(self.mqtt_ip, 1883, 60)
		data = hex_to_string(scan_tag_capture())
		client.publish(self.reader_id+"/data",data,qos=0,retain=False)
		client.loop_forever()
	def hex_to_string(self,value):
		if value[0]==set():
			pass
		else:
			filter1=value[0]
			ss=str(filter1)
			cc=ss[2:-2]
			print(cc)
			b=bytes.fromhex(cc)
			return b.decode()
