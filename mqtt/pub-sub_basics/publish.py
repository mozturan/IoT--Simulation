import time
from paho.mqtt import client as mqtt_client
from pyspectator.processor import Cpu
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

#* GETS CPU TEMP AS STATUS
def publish(client):
     msg_count = 0
     while True:
        cpu = Cpu(monitoring_latency=1) #changed here
        time.sleep(1)
        msg = f"{cpu.temperature}"
        result = client.publish(topic, msg)
        #* result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()


