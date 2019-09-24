import time
import paho.mqtt.client as paho
import random
import decimal

broker="m2m.eclipse.org"
broker="localhost"

def on_message(client, userdata, msg):
    if msg.payload.decode('utf-8') == "Ligar":
        global t1_status
        t1_status = True
        client.publish("/Sensores/Temperatura", t1_status)#publish
        time.sleep(3)
    elif msg.payload.decode("utf-8") == "Desligar":
        t1_status = False
        client.publish("/Sensores/Temperatura", t1_status)#publish
        time.sleep(3)

t1_ligada = True
t1_temper = 0
t1_status = ""

client = paho.Client("termometer-001")
client.on_message = on_message
print("Conectando ao broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("Enviando temperatura")

random.seed()
try:
    while (True):
        print()
        if t1_ligada == True:
            t1_status = "Ligada"
            t1_temper = 24
        elif t1_ligada == False:
            t1_status = "Desligada"
            t1_temper = 0
        client.publish("/Temperatura/",str(t1_temper)+'°C')#publish
        time.sleep(2.5)

except KeyboardInterrupt:
    client.publish("/Temperatura/",0)#publish
    print("\nDesconectado.")
client.disconnect() #disconnect
client.loop_stop() #stop loop
