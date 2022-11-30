from tkinter import *
from paho.mqtt import client as mqtt_client
import random
from paho import mqtt

broker = 'e9a907584e984fd6a82dc5fa0408e996.s2.eu.hivemq.cloud'
port = 8883
topic = "cpu/tempeture"
topic_sub = "api/notification/37/#"
client_id = ''
username = 'tinrafiq'
password = "j8ktX@W7'Qw"


def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
 
 
    client = mqtt_client.Client(client_id)

    #* enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)


    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        temp_label.config(text=f"{msg.payload.decode()}",
                        fg="black")


    client.subscribe(topic)
    client.on_message = on_message


window = Tk()
window.title("Tempeture of CPU")
window.geometry('256x256')
window.resizable(False,False)
window.configure(bg="white")
canvas = Canvas(window, bg="white", width=256,height=256)
canvas.place(x=0,y=0)
img = PhotoImage(file="thermometer.png")
canvas.create_image(0,0,anchor=NW,image=img)

is_on = False

 
# Create Label
temp_label = Label(window,
                 text=" °C",
                 bg="white",
                 fg="black",
                 font=("Helvetica", 32))
 
temp_label.place(x=150,y=100)

client = connect_mqtt()
subscribe(client)
client.loop_start()

window.mainloop()
client.loop_stop()

