import paho.mqtt.client as mqtt
import subprocess
import threading
import time

class Controller:
	broker="m2m.eclipse.org"
	broker="localhost"

	def on_connect(client, userdata, flags, rc):
    		client.subscribe('/Dispositivos/#')

	def on_message(client, userdata, msg):
    		print(msg.topic + ' - ' + str(msg.payload.decode('utf-8')))

	
	client = mqtt.Client()
	client.on_connect = on_connect
	print("Conectando ao broker",broker)
	time.sleep(2)
	client.on_message = on_message

	client.connect(broker)

	client.loop_forever()