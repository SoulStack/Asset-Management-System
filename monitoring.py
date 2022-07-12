import os
from time import sleep
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect('10.0.2.19', 1887,65535)
def on_connect(client,userdata,flags,rc):
	print("Connected with return code "+ str(rc))
def on_message(client,userdata,msg) :
	print(msg.topic + " " + str(msg.payload))

client.on_connect = on_connect
client.on_message = on_message

while True :
	sleep(5)


	campus20_status = os.system('sudo systemctl is-active --quiet campus20')
	print("status of campus20",campus20_status)
	if campus20_status == 0 :
		msg = json.dumps({"name of the service" : "campus20","type" : "Backend","Status" : "Active"});
		print(msg)
		client.publish("campus20",payload = msg,qos =1 ,retain= False)
	else :
		msg = json.dumps({"name of the service" : "campus20","type" : "Backend","Status" : "Not Active"});
		client.publish("campus20",payload = msg,qos =1 ,retain= False)


	campus6_status = os.system('sudo systemctl is-active --quiet campus6')
	print("status of campus6",campus6_status)
	if campus6_status == 0 :
		msg = json.dumps({"name of the service" : "campus6","type" : "Backend","Status" : "Active"});
		client.publish("campus6",payload = msg,qos =1 ,retain= False)
	else :
		msg = json.dumps({"name of the service" : "campus6","type" : "Backend","Status" : "Not Active"});
		client.publish("campus6",payload = msg,qos =1 ,retain= False)

	campus6_2_status = os.system('sudo systemctl is-active --quiet campus6_2')
	print("status of campus6_2 :" ,campus6_2_status)
	if campus6_2_status == 0 :
		msg = json.dumps({"name of the service" : "campus6_2","type" : "Backend","Status" : "Active"});
		client.publish("campus6_2",payload = msg,qos =1 ,retain= False)
	else :
		msg = json.dumps({"name of the service" : "campus6_2","type" : "Backend","Status" : "Not Active"});
		client.publish("campus6_2",payload = msg,qos =1 ,retain= False)

	campus12_status = os.system('sudo systemctl is-active --quiet campus12')
	print("status of campus12 :",campus12_status)
	if campus12_status == 0 :
		msg = json.dumps({"name of the service" : "campus12","type" : "Backend","Status" : "Active"});
		client.publish("campus12",payload = msg,qos =1 ,retain= False)
	else :
		msg = json.dumps({"name of the service" : "campus12","type" : "Backend","Status" : "Not Active"});
		client.publish("campus12",payload = msg,qos =1 ,retain= False)

	campus8_status = os.system('sudo systemctl is-active --quiet campus8')
	print("status of campus8 :",campus8_status)
	if campus8_status == 0 :
		msg = json.dumps({"name of the service" : "campus8","type" : "Backend","Status" : "Active"});
		client.publish("campus8",payload = msg,qos =1 ,retain= False)
	else :
		msg = json.dumps({"name of the service" : "campus8","type" : "Backend","Status" : "Not Active"});
		client.publish("campus8",payload = msg,qos =1 ,retain= False)



    
