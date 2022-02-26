from rfid_reader import RFIDReader
#log1
import paho.mqtt.client as mqtt
# iniate
import json
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
#log2

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#log3
client.connect("192.168.0.100", 1883, 60)
#log4

#log6
topic = "reader1/data"
reader = RFIDReader('socket', host="192.168.0.250", port=27011, addr="00")
#connect
reader.connect()
info = reader.getInfo()
print("INFO ", info)
while True:
	tags = reader.scantags()
	print(set(tags))
	b=json.dumps(tags)
	client.publish(topic, payload=b, qos=2, retain=False)
	client.loop_forever()
