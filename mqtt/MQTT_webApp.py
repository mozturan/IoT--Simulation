import datetime
import time
import streamlit as st
    #* to read json file
    #* to create delay (additionally)
    #* to create a client and connect to broker
from paho.mqtt import client as mqtt_client
    #* to use tls
from paho import mqtt
from firebase import firebase
import sys
import numpy as np

broker = 'e9a907584e984fd6a82dc5fa0408e996.s2.eu.hivemq.cloud'
port = 8883
topic = "xbee"
topic_sub = "api/notification/37/#"
client_id = ''
username = 'tinrafiq'
password = "j8ktX@W7'Qw"
firebase = firebase.FirebaseApplication('https://iot-mqtt-now-default-rtdb.europe-west1.firebasedatabase.app', None)

global sensor_2, sensor_6, sensor_8, sensor_14
sensor_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sensor_6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sensor_8 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sensor_14 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

global mess
mess = []


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

            if msg.topic:
                #* sensor_id, generated_time, value, saved_time, send_time
                temp = msg.payload.decode()
                temp = temp.split() 
                received = [(temp[4]), str(datetime.datetime.now().time())]
                sensor_id = temp[0]
                value = temp[2]

                #! burayı aç
                if int(sensor_id) == 2:
                    sensor_2.append(int(value))
                elif int(sensor_id) == 6:
                    sensor_6.append(int(value))
                elif int(sensor_id) == 8:
                    sensor_8.append(int(value))
                elif int(sensor_id) == 14:
                    sensor_14.append(int(value))
                else: st.write("Error")

                #! burayı aç
                mess.append(received)
                global val
                val = str(value)

            #? send to firebase
            if val != '':
 
                firebase.post('/xbee', temp)
                val = ''

        #* subscribe to a certain topic and print it
        client.subscribe(topic, qos=0)
        client.on_message = on_message

def main():
    title = st.sidebar.title("**Welcome, You can connect to my MQTT-ZigBEE Simulation with this Web App**")
    context = st.sidebar.subheader("**YOu can get Sensor Values via MQTT and visualize them**")
    text = st.sidebar.subheader("**To connect to MQTT broker by default settings click on 'Connect' button**")

    button_connect = st.sidebar.button('Connect and Subscribe')

    #* to visiualize values
    area_1 = st.empty()
    area_2a = st.empty()
    area_2 = st.empty()
    area_3a = st.empty()
    area_3 = st.empty()
    area_4a = st.empty()
    area_4 = st.empty()
    area_5a = st.empty()
    area_5 = st.empty()


    if button_connect:

        st.subheader("We also send data to Firebase Realtime DB")
        area_1.markdown("![Alt Text](https://wp-technique.com/loading/loading.gif)")
        client = connect_mqtt()
        subscribe(client)
        client.loop_start()

        area_1.header("Sensor Values (Realtime)")
        area_2a.subheader("Sensor A Values")
        area_3a.subheader("Sensor B Values")
        area_4a.subheader("Sensor C Values")
        area_5a.subheader("Sensor D (DIGITAL) Values")


        while button_connect==True:

                # with open("C:\\Users\\tinrafiq\\Documents\\mqtt\\mqtt\\mqtt\\data.txt", "w+") as txt_file:
                #     txt_file.write(str(np.array(mess)))
                time.sleep(1)
                #! burayı aç
                area_2.line_chart(sensor_2[-10:])
                area_3.line_chart(sensor_6[-10:])
                area_4.line_chart(sensor_8[-10:])
                if sensor_14[-1] == 0:
                    area_5.markdown("![Alt Text](https://upload.wikimedia.org/wikipedia/commons/d/dd/Icon_Transparent_Red.png)")
                else:
                    area_5.markdown("![Alt Text](https://upload.wikimedia.org/wikipedia/commons/b/b0/Icon_Transparent_Green.png)")


if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print("\nPrograms was stopped")  
        sys.exit()

