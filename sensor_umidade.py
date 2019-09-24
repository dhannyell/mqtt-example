import time
import paho.mqtt.client as paho
import random
import decimal

broker="m2m.eclipse.org"
broker="localhost"

client= paho.Client("humidity-001")

print("Conectando ao broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("Enviando umidade")

try:
    while (True):
        humid = random.uniform(34.0, 40.0)
        humid = decimal.Decimal(humid).quantize(decimal.Decimal('.01'))
        client.publish("/Umidade/",str(humid)+'%')#publish
        time.sleep(2.5)
except KeyboardInterrupt:
    client.publish("/Umidade/",0)#publish
    print("\nDesconectado.")

client.disconnect() #disconnect
client.loop_stop() #stop loop
