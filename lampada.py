import time
import paho.mqtt.client as paho

def on_message(client, userdata, msg):
    if msg.payload.decode('utf-8') == "Ligar":
        global l1_status
        l1_status = True
        client.publish("/Lampadas/L1", l1_status)#publish
        time.sleep(3)
    elif msg.payload.decode("utf-8") == "Desligar":
        l1_status = False
        client.publish("/Lampadas/L1", l1_status)#publish
        time.sleep(3)

broker="m2m.eclipse.org"
broker="localhost"

l1_status = True

client= paho.Client("lamp-001")
client.on_message = on_message
print("Conectando ao broker",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
# Inscrevendo no Controlador
print("Inscrevendo no Controlador")
client.subscribe("/Dispositivos/Lampadas/L1")#subscribe
time.sleep(2)

print("Enviando status da lâmpada.")
try:
     while (True):
        print()
        if l1_status == True:
            l_status = "Ligada"
        elif l1_status == False:
            l_status = "Desligada"
        client.publish("/Lampadas/L1", l_status)#publish
        time.sleep(60*1) #Espera 1 minuto

except KeyboardInterrupt:
    print("\nDesconectado.")
client.disconnect() #disconnect
client.loop_stop() #stop loop
