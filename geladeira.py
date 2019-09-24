import time
import paho.mqtt.client as paho
import random
import decimal

broker="m2m.eclipse.org"
broker="localhost"

def on_message(client, userdata, msg):
    if msg.payload.decode('utf-8') == "Aberta":
        global l1_status
        l1_status = True
        client.publish("/Geladeira/", l1_status)#publish
        time.sleep(3)
    elif msg.payload.decode("utf-8") == "Fechada":
        l1_status = False
        client.publish("/Geladeira/", l1_status)#publish
        time.sleep(3)

gel_aberta = True
gel_status = ""

client= paho.Client("geladeira")
client.on_message = on_message
print("Conectando ao broker",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
# Inscrevendo no Controlador
print("Inscrevendo no Controlador")
time.sleep(2)
print("Enviando status da Geladeira.")

try:
     while (True):
        print()
        if gel_aberta == True:
            gel_status = 'Aberta'
        elif gel_aberta == False:
            gel_status = 'Fechada'
        client.publish("/Geladeira/", gel_status)#publish
        time.sleep(60*1) #Espera 1 minuto

except KeyboardInterrupt:
    print("\nDesconectado.")
    client.publish("/Geladeira/", "Fechada")#publish
client.disconnect() #disconnect
client.loop_stop() #stop loop
