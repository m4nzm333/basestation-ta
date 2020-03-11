# Copyright (c) 2020 m4nzm333
# Source code for receive data from Sensor Node
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import paho.mqtt.client as mqtt
import datetime as datetime
import logging

# Class for Raspberry Subscriber
class RaspiSubscriber:

    # Instance Attribute
    def __init__(self, mqttServer, mqttPort, clientName):
        logging.basicConfig(filename='subscriber.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
        keepAliveInterval = 45
        mqttTopic = [("temperature", 0),("pressure", 0),("hummidity", 0)]

        mqttClient = mqtt.Client(clientName)

        # Assign Event Callbacks
        mqttClient.on_message = self.on_message
        mqttClient.on_subscribe = self.on_subscribe
        mqttClient.on_connect = self.on_connect

        # Connect
        logging.info("Connecting to MQTT Broker({:s}:{:s}).".format(mqttServer, str(mqttPort)))
        print("Connecting to MQTT Broker({:s}:{:s}).".format(mqttServer, str(mqttPort)))
        try:
            mqttClient.connect(mqttServer, mqttPort, keepAliveInterval)
        except:
            logging.exception("MQTT Broker({:s}:{:s}) connection failed caused by timeout.".format(mqttServer, str(mqttPort)))
        mqttClient.subscribe(mqttTopic)

        #Continue the network loop
        mqttClient.loop_forever()
    
    # Read Data Function
    def on_message(self, mosq, obj, msg):
        logging.info("Message received from topic {:s}".format(msg.topic))
        print("============================")
        print("Timestamp : " + str(datetime.datetime.now()))
        print("Topic     : " + msg.topic)
        print("Payload   : " + msg.payload.decode('utf-8'))
        print("\n")
        # TODO : Add saveToArchive funtion

    # Show error if connection unsuccessful
    def on_connect(self, client, userdata, flag, rc):
        if rc==0:
            logging.info("Connection successful. Waiting for data.")
            print("Connection successful. Waiting for data.")
        if rc==1:
            logging.error("Connection refused - incorrect protocol version.")
            print("Connection refused - incorrect protocol version")
        if rc==2:
            logging.error("Connection refused - invalid client identifier.")
            print("Connection refused - invalid client identifier.")
        if rc==3:
            logging.error("Connection refused - server unavailable.")
            print("Connection refused - server unavailable.")
        if rc==4:
            logging.error("Connection refused - not authorised.")
            print("Connection refused - not authorised.")

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        logging.info('Subscribe to {:s}'.format(str(mosq.topic)))
        print('Subscribe to {:s}'.format(str(mosq.topic)))
        pass
