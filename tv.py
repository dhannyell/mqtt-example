import time
import paho.mqtt.client as paho
import random
import decimal

broker="m2m.eclipse.org"
broker="localhost"

def on_message(client, userdata, msg):
    if msg.payload.decode('utf-8') == "Ligar":
        global tv_status
        tv_status = True
        client.publish("/TV", tv_status)#publish
        time.sleep(3)
    elif msg.payload.decode("utf-8") == "Desligar":
        tv_status = False
        client.publish("/TV", tv_status)#publish
        time.sleep(3)

tv_ligada = True
tv_status = ""
tv_canal = 1
tv_volume = 0

client = paho.Client("tv")
client.on_message = on_message
print("Conectando ao broker",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
# Inscrevendo no Controlador
print("Inscrevendo no Controlador")
time.sleep(2)
print("Enviando status da TV.")

try:
     while (True):
        print()
        if tv_ligada == True:
            tv_status = "Ligada"
            tv_canal = 12
            tv_volume = 19
        elif tv_ligada == False:
            tv_status = "Desligada"
        #tv_volume = decimal.Decimal(tv_volume).quantize(decimal.Decimal('.01'))
        client.publish("/TV/Canal",str(tv_canal))#publish
        client.publish("/TV/Volume",str(tv_volume))#publish
        time.sleep(60*1) #Espera 1 minuto

except KeyboardInterrupt:
    print("\nDesconectado.")
    client.publish("/TV/", "Desligada")#publish
client.disconnect() #disconnect
client.loop_stop() #stop loop
