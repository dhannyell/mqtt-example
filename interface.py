import ssl
import sys

import time
from PIL import ImageTk, Image
import paho.mqtt.client
import paho.mqtt.publish

from tkinter import *

def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='/Lampadas/L1')
    client.subscribe(topic='/Umidade/')
    client.subscribe(topic='/Temperatura/')
    client.subscribe(topic='/Geladeira/')
    client.subscribe(topic='/TV/')

lampada_message_var = False
umidade_message_var = False
umidade_value = 0
temperatura1_message_var = False
temperatura1_temp_var = 0
tv_message_var = False
tv_canal_var = 1
tv_volume_var = 0
geladeira_message_var = False

def on_message(mosq, obj, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))

def on_message_temperatura1(client, userdata, message):
    global temperatura1_message_var
    global temperatura1_temp_var
    temperatura1_message_var = str(message.payload.decode("utf-8"))
    temperatura1_temp_var = int(temperatura1_temp_var)

def on_message_geladeira(client, userdata, message):
    global geladeira_message_var
    if str(message.payload.decode("utf-8")) == 'Aberta':
        geladeira_message_var = True
    elif str(message.payload.decode('utf-8')) == 'Fechada':
        geladeira_message_var = False

def on_message_tv(client, userdata, message):
    global tv_message_var
    if str(message.payload.decode("utf-8")) == 'Ligada':
        tv_message_var = True
    elif str(message.payload.decode("utf-8")) == 'Desligada':
        tv_message_var = False

def on_message_umidade(client, userdata, message):
    global umidade_message_var
    umidade_message_var = str(message.payload.decode("utf-8"))

def on_message_lampada(client, userdata, message):
    global lampada_message_var
    if str(message.payload.decode("utf-8")) == 'Ligada':
        lampada_message_var = True
    elif str(message.payload.decode("utf-8")) == 'Desligada':
        lampada_message_var = False



#============================Temperatura Button===================================
def on_button_temperatura1():
    global temperatura1_message_var
    global client

    if temperatura1_message_var:
        client.publish("/Dispositivos/Sensores/Temperatura", 'Desligar')
        temperatura1_message_var = False
    elif not temperatura1_message_var:
        client.publish("/Dispositivos/Sensores/Temperatura", 'Ligar')
        temperatura1_message_var = True

def on_button_temperatura1_aumentar():
    global temperatura1_message_var
    global temperatura1_temp_var
    global client

    if temperatura1_message_var:
        temperatura1_temp_var += 1

def on_button_temperatura1_diminuir():
    global temperatura1_message_var
    global temperatura1_temp_var
    global client

    if temperatura1_message_var:
        temperatura1_temp_var = int(temperatura1_temp_var) - 1

#============================Umidade Button===================================
def on_button_umidade():
    global umidade_message_var
    global client

    if umidade_message_var:
        client.publish("/Dispositivos/Sensores/Umidade", 'Desligar')
        umidade_message_var = False
    elif not umidade_message_var:
        client.publish("/Dispositivos/Sensores/Umidade", 'Ligar')
        umidade_message_var = True

#============================Lampada Button===================================
def on_button_lampada():
    global lampada_message_var
    global client

    if lampada_message_var:
        client.publish("/Dispositivos/Lampadas/L1", 'Desligar')
        lampada_message_var = False
    elif not lampada_message_var:
        client.publish("/Dispositivos/Lampadas/L1", 'Ligar')
        lampada_message_var = True

#============================TV Button===================================
def on_button_tv():
    global tv_message_var
    global client

    if tv_message_var:
        tv_message_var = False
        client.publish('/Dispositivos/TV/', 'Desligar')
    elif not tv_message_var:
        tv_message_var = True
        client.publish('/Dispositivos/TV/', 'Ligar')

def on_button_tv_canal_mais():
    global tv_message_var
    global tv_canal_var
    global client

    if tv_message_var:
        tv_canal_var += 1

def on_button_tv_canal_menos():
    global tv_message_var
    global tv_canal_var
    global client

    if tv_message_var:
        if tv_canal_var > 1:
            tv_canal_var -= 1

def on_button_tv_volume_mais():
    global tv_message_var
    global tv_volume_var
    global client

    if tv_message_var:
        if tv_volume_var < 30:
            tv_volume_var += 1

def on_button_tv_volume_menos():
    global tv_message_var
    global tv_volume_var
    global client

    if tv_message_var:
        if tv_volume_var > 0:
            tv_volume_var -= 1



#lampada_message_var = False
#umidade_message_var = False
#umidade_value = 23
#temperatura1_message_var = False
#temperatura1_temp_var = 24
#tv_message_var = False
#tv_canal_var = 11
#tv_volume_var = 11
#geladeira_message_var = False




client = paho.mqtt.client.Client(client_id='1', clean_session=False)
client.connect(host='localhost', port=1883)

client.on_connect = on_connect
client.message_callback_add('/Temperatura/', on_message_temperatura1)
client.message_callback_add('/Geladeira/', on_message_geladeira)
client.message_callback_add('/Lampadas/L1', on_message_lampada)
client.message_callback_add('/Umidade/', on_message_umidade)
client.message_callback_add('/TV/', on_message_tv)
client.on_message = on_message

def main():

    root = Tk()
    root.title("MQTT")

    #============================Temperatura+++++===================================
    temperatura_sala = Frame(root)
    temperatura_sala.pack(side=LEFT)

    temperatura_title_sala = Label(temperatura_sala, text='Temperatura')
    temperatura_title_sala["font"] = ("Helvetica", "14", "bold")
    temperatura_title_sala.pack()

    temperatura_status = Label(temperatura_sala, text='---')
    temperatura_status['font'] = ('Helvetica', 12)
    temperatura_status.pack()

    temperatura_message_sala = Label(temperatura_sala, text='Valor do Sensor')
    temperatura_message_sala["font"] = ("Helvetica", "12")
    temperatura_message_sala.pack()

    temperatura_sala_button = Button(temperatura_sala)
    temperatura_sala_button["text"] = "Ligar!"
    temperatura_sala_button["font"] = ("Helvetica", "10")
    temperatura_sala_button["width"] = 7
    temperatura_sala_button["command"] = on_button_temperatura1
    temperatura_sala_button.pack(side=LEFT)

    temperatura_sala_button_1 = Button(temperatura_sala)
    temperatura_sala_button_1['text'] = '+'
    temperatura_sala_button_1['font'] = ('Helvetica', 10)
    temperatura_sala_button_1['width'] = 2
    temperatura_sala_button_1['command'] = on_button_temperatura1_aumentar
    temperatura_sala_button_1.pack(side=RIGHT, anchor="n")

    temperatura_sala_button_2 = Button(temperatura_sala)
    temperatura_sala_button_2['text'] = '-'
    temperatura_sala_button_2['font'] = ('Helvetica', 10)
    temperatura_sala_button_2['width'] = 2
    temperatura_sala_button_2['command'] = on_button_temperatura1_diminuir
    temperatura_sala_button_2.pack(side=RIGHT, anchor="s")

    #============================Sensor de Umidade==================================
    umidade = Frame(root, padx=40, pady=10)
    umidade.pack(side=LEFT)

    umidade_title = Label(umidade, text='Umidade')
    umidade_title["font"] = ("Helvetica", "14", "bold")
    umidade_title.pack()

    umidade_status = Label(umidade, text='---')
    umidade_status["font"] = ("Helvetica", "12")
    umidade_status.pack()

    umidade_message = Label(umidade, text='Valor do Sensor')
    umidade_message["font"] = ("Helvetica", "12")
    umidade_message.pack()

    umidade_button = Button(umidade)
    umidade_button["text"] = "Ligar!"
    umidade_button["font"] = ("Helvetica", "10")
    umidade_button["width"] = 7
    umidade_button["command"] = on_button_umidade
    umidade_button.pack(side=BOTTOM)

    #============================Lâmpada===========================================
    lampada = Frame(root, padx=40, pady=10)

    lampada.pack(side=LEFT)

    lampada_title = Label(lampada, text='Lampada')
    lampada_title["font"] = ("Helvetica", "14", "bold")
    lampada_title.pack()

    lampada_message = Label(lampada, text='Status')
    lampada_message["font"] = ("Helvetica", "12")
    lampada_message.pack()

    lampada_button = Button(lampada)
    lampada_button["text"] = "Ligar!"
    lampada_button["font"] = ("Helvetica", "10")
    lampada_button["width"] = 7
    lampada_button["command"] = on_button_lampada
    lampada_button.pack(side=BOTTOM)


    #============================TV================================================
    tv = Frame(root, padx=40, pady=10)
    tv.pack(side=LEFT)

    tv_title = Label(tv, text='TV')
    tv_title["font"] = ("Helvetica", "14", "bold")
    tv_title.pack()

    tv_message = Label(tv, text='Status')
    tv_message["font"] = ("Helvetica", "12")
    tv_message.pack()

    tv_channel = Label(tv, text='Valor')
    tv_channel["font"] = ("Helvetica", "12")
    tv_channel.pack()

    tv_volume = Label(tv, text='Valor')
    tv_volume["font"] = ("Helvetica", "12")
    tv_volume.pack()

    tv_button = Button(tv)
    tv_button['text'] = 'Ligar!'
    tv_button['font'] = ('Helvetica', 10)
    tv_button['width'] = 7
    tv_button['command'] = on_button_tv
    tv_button.pack(side=LEFT)

    tv_button_1 = Button(tv)
    tv_button_1['text'] = 'C+'
    tv_button_1['font'] = ('Helvetica', 10)
    tv_button_1['width'] = 2
    tv_button_1['command'] = on_button_tv_canal_mais
    tv_button_1.pack(side=LEFT)

    tv_button_2 = Button(tv)
    tv_button_2['text'] = 'C-'
    tv_button_2['font'] = ('Helvetica', 10)
    tv_button_2['width'] = 2
    tv_button_2['command'] = on_button_tv_canal_menos
    tv_button_2.pack(side=LEFT)

    tv_button_3 = Button(tv)
    tv_button_3['text'] = 'V+'
    tv_button_3['font'] = ('Helvetica', 10)
    tv_button_3['width'] = 2
    tv_button_3['command'] = on_button_tv_volume_mais
    tv_button_3.pack(side=RIGHT)

    tv_button_4 = Button(tv)
    tv_button_4['text'] = 'V-'
    tv_button_4['font'] = ('Helvetica', 10)
    tv_button_4['width'] = 2
    tv_button_4['command'] = on_button_tv_volume_menos
    tv_button_4.pack(side=RIGHT)

    #=======================Geladeira=++==========================================
    geladeira = Frame(root, padx=40, pady=0)
    geladeira.pack(side=LEFT)

    geladeira_title = Label(geladeira, text='Geladeira')
    geladeira_title["font"] = ("Helvetica", "14", "bold")
    geladeira_title.pack()

    geladeira_message = Label(geladeira, text='Status')
    geladeira_message["font"] = ("Helvetica", "12")
    geladeira_message.pack()




    while True:
        root.update()
        client.loop(.1)
        umidade_message.configure(text=umidade_message_var)
        tv_message.configure(text=tv_message_var)
        temperatura_message_sala.configure(text=temperatura1_message_var)
        geladeira_message.configure(text=geladeira_message_var)

        client.publish("/Dispositivos/Umidade/1", umidade_message_var)
        client.publish("/Dispositivos/Temperatura/1", temperatura1_message_var)

        if not temperatura1_message_var:
            temperatura_status.configure(text='Status: Offline', fg='red')
            temperatura_sala_button.configure(text='Ligar')
        elif temperatura1_message_var:
            temperatura_status.configure(text='Status: Online', fg='green')
            temperatura_sala_button.configure(text='Desligar')

        if not umidade_message_var:
            umidade_status.configure(text="Status: Offline", fg="red")
            umidade_button.configure(text='Ligar')
        elif umidade_message_var:
            umidade_status.configure(text="Status: Online", fg="green")
            umidade_button.configure(text='Desligar')

        if tv_message_var:
            tv_message.configure(text='Status: Ligada2', fg='green')
            tv_button.configure(text='Desligar')
            tv_channel.configure(text='Canal: '+ str(tv_canal_var))
            tv_volume.configure(text='Volume: '+ str(tv_volume_var))
        elif not tv_message_var:
            tv_message.configure(text='Status: Desligada', fg='red')
            tv_button.configure(text='Ligar')
            tv_channel.configure(text='Canal: --')
            tv_volume.configure(text='Volume: --')

        if lampada_message_var:
            lampada_message.configure(text='Status: Ligada', fg='green')
            lampada_button.configure(text='Desligar')
        elif not lampada_message_var:
            lampada_message.configure(text='Status: Desligada', fg='red')
            lampada_button.configure(text='Ligar')

        if geladeira_message_var:
            geladeira_message.configure(text='Status: Aberta', fg='green')
        elif not geladeira_message_var:
            geladeira_message.configure(text='Status: Fechada', fg='red')



if __name__ == '__main__':
	main()
	sys.exit(0)
