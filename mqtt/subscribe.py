import random
from paho.mqtt import client as mqtt_client
from paho import mqtt

broker = 'e9a907584e984fd6a82dc5fa0408e996.s2.eu.hivemq.cloud'
port = 8883
topic = "cpu/tempeture"
topic_sub = "api/notification/37/#"
client_id = ''
username = 'tinrafiq'
password = "j8ktX@W7'Qw"

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
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    #* subscribe to a certain topic and print it
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
