# Copyright (c) 2020 m4nzm333
# Source code for receive data from Sensor Node
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import paho.mqtt.client as mqtt
import datetime as datetime

# Class for Raspberry Subscriber
class RaspiSubscriber:

    # Instance Attribute
    def __init__(self, mqttServer, mqttPort, clientName):
        keepAliveInterval = 45
        mqttTopic = [("temperature", 0),("pressure", 0),("hummidity", 0)]

        mqttClient = mqtt.Client(clientName)

        # Assign Event Callbacks
        mqttClient.on_message = self.on_message
        mqttClient.on_subscribe = self.on_subscribe
        mqttClient.on_connect = self.on_connect

        # Connect
        print("Connecting to MQTT Broker({:s}:{:s}).".format(mqttServer, str(mqttPort)))
        mqttClient.connect(mqttServer, mqttPort, keepAliveInterval)
        mqttClient.subscribe(mqttTopic)

        #Continue the network loop
        mqttClient.loop_forever()
    
    # Read Data Function
    def on_message(self, mosq, obj, msg):
        print("============================")
        print("Timestamp : " + str(datetime.datetime.now()))
        print("Topic     : " + msg.topic)
        print("Payload   : " + msg.payload.decode('utf-8'))
        print("\n")
        # TODO : Add saveToArchive funtion

    # Show error if connection unsuccessful
    def on_connect(self, client, userdata, flag, rc):
        if rc==0:
            print("Connection successful. Waiting for data.")
        if rc==1:
            print("Connection refused - incorrect protocol version\n")
        if rc==2:
            print("Connection refused - invalid client identifier\n")
        if rc==3:
            print("Connection refused - server unavailable\n")
        if rc==4:
            print("Connection refused - not authorised\n")

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print(str(mosq.topic))
        pass
