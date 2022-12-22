import time
import streamlit as st
    #* to read json file
    #* to create delay (additionally)
    #* to create a client and connect to broker
from paho.mqtt import client as mqtt_client
    #* to use tls
from paho import mqtt
    #* to get cpu heat
    #* just some make-up
from firebase import firebase
import sys

broker = 'e9a907584e984fd6a82dc5fa0408e996.s2.eu.hivemq.cloud'
port = 8883
topic = "xbee"
topic_sub = "api/notification/37/#"
client_id = ''
username = 'tinrafiq'
password = "j8ktX@W7'Qw"
firebase = firebase.FirebaseApplication('https://iot-mqtt-now-default-rtdb.europe-west1.firebasedatabase.app', None)

global db
db= [0 , 0]

global mess
mess = [0, 0]

def connect_mqtt():

        #* RC returns either zero or one due to connection status
        def on_connect(client, userdata, flags, rc):
            if rc==0:
                st.sidebar.header("**CONNECTED TO THE MQTT BROKER**")
            else:
                st.sidebar.header("**CONNECTION FAILED**")

        #* set as a client (node)
        client = mqtt_client.Client(client_id)

        #* enable TLS for secure connection
        #* some mqtt broker services use this
        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        #* Broker login infos
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

def subscribe(client: mqtt_client):

        def on_message(client, userdata, msg):
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            if msg.topic == "xbee":
                temp = msg.payload.decode() 
                db.append(temp)
                mess.append(msg)
                
                global val
                val = str(temp)

            if val != '':
 
                firebase.post('/xbee', temp)
                val = ''

        #* subscribe to a certain topic and print it
        client.subscribe(topic)
        client.on_message = on_message

def main():
    title = st.sidebar.title("**Welcome, You can connect to my MQTT Simulation with this Web App**")
    context = st.sidebar.subheader("**With MQTT I'am publishing my CPU Temperature to a MQTT Broker. This Web App is a client subscribing to the topic which is published by my computer client.**")
    text = st.sidebar.subheader("**To connect to MQTT broker by default settings click on 'Connect' button**")

    button_connect = st.sidebar.button('Connect and Subscribe')
    area_1 = st.empty()
    area_2 = st.empty()
    # image = Image.open("MQTT/spinner2.gif")
    if button_connect:
        st.subheader("We also send data to Firebase Realtime DB")
        area_1.markdown("![Alt Text](https://wp-technique.com/loading/loading.gif)")
        client = connect_mqtt()
        subscribe(client)
        # client.loop_forever()

        while True:
            client.loop()
            area_1.metric(label="Value", value=str((db[-1])))
            
if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("\nPrograms was stopped")  
        sys.exit()

