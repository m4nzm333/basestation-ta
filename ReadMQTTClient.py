# Copyright (c) 2020 m4nzm333
# Source code for receive data from Sensor Node
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import paho.mqtt.client as mqtt
import datetime as datetime
import ArchiveData as archiveData 

# MQTT Setting
MQTT_Broker = "192.168.1.5"
MQTT_Port = 1883
Keep_Alive_Interval = 45
# MQTT multi topic for subscribe
MQTT_Topic = [("temperature", 0),("pressure", 0),("hummidity", 0)]

mqttc = mqtt.Client("Basestation-0001")
# Read Data Function
def on_message(mosq, obj, msg):
    print("============================")
    print("Timestamp : " + str(datetime.datetime.now()))
    print("Topic     : " + msg.topic)
    print("Payload   : " + msg.payload.decode('utf-8'))
    print("\n")
    # TODO : Add saveToArchive funtion
    archiveData.saveJsonIntoFile(msg.payload.decode('utf-8'))

def on_subscribe(mosq, obj, mid, granted_qos):
    print(str(mosq.topic))
    pass

# Show error if connection unsuccessful
def on_connect(client, userdata, flag, rc):
    if rc==0:
        print("Connection successful\n")
    if rc==1:
        print("Connection refused - incorrect protocol version\n")
    if rc==2:
        print("Connection refused - invalid client identifier\n")
    if rc==3:
        print("Connection refused - server unavailable\n")
    if rc==4:
        print("Connection refused - not authorised\n")

print("Connection to Broker with Address " + str(MQTT_Broker) + ":" + str(MQTT_Port))
print("==================================")


def main():
    # Assign Event Callbacks
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_connect = on_connect

    # Connect
    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    mqttc.subscribe(MQTT_Topic)

    #Continue the network loop
    mqttc.loop_forever()

main()