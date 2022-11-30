"""
"""
#* to read json file
import json
#* to create delay (additionally)
import time
#* to create a client and connect to broker
from paho.mqtt import client as mqtt_client
#* to use tls
from paho import mqtt
#* to get cpu heat
from pyspectator.processor import Cpu
#* just some make-up
import sys

from firebase import firebase

firebase = firebase.FirebaseApplication('https://iot-mqtt-now-default-rtdb.europe-west1.firebasedatabase.app', None)

#* Gets broker info from json file
broker_ = json.load(open("mqtt/broker.json"))

#* Gives client we created an id and identify subscribing topic
client_id = "001"
topic = "cpu/tempeture"

def connect_mqtt():

    #* RC returns either zero or one due to connection status
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
 
    #* set as a client (node)
    client = mqtt_client.Client(client_id)

    #* enable TLS for secure connection
    #* some mqtt broker services use this
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    #* Broker login infos
    client.username_pw_set(broker_["username"], broker_["password"])
    client.on_connect = on_connect
    client.connect(broker_["broker"], broker_["port"])
    return client

def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        temp = 0

        if msg.topic == "cpu/tempeture":
            temp = str(msg.payload, 'UTF-8')
            temp = temp.strip()
            print(temp)
            global val
            val = temp

        if val != '':    
            print(val)
            data = val
            firebase.post('/cpu/tempeture', val)
            val = ''

    #* subscribe to a certain topic and print it
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        print("\nPrograms was stopped")  
        sys.exit()

