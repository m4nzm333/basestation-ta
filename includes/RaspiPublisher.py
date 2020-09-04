# Copyright (c) 2020 m4nzm333
# Source code for sending data log to server
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import paho.mqtt.client as mqtt
import datetime as datetime
from time import sleep
import logging

# Class for Raspberry Pi Publisher
class RaspiPublisher:

    mqttClient = mqtt.Client()
    
    # Instance Attribute
    def __init__(self, mqttServer, mqttPort, clientName):
        logging.basicConfig(filename='./log/publisher.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
        keepAliveInterval = 60

        self.mqttClient = mqtt.Client(clientName)

        # Assign Event Callbacks
        self.mqttClient.on_publish = self.on_publish
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_disconnect = self.on_disconnect

        # Connecting
        logging.info("Connecting to MQTT Broker({:s}:{:s}).".format(mqttServer, str(mqttPort)))
        print("Connecting to MQTT Broker({:s}:{:s}).".format(mqttServer, str(mqttPort)))
        try:
            self.mqttClient.connect(mqttServer, mqttPort, keepAliveInterval)
        except:
           logging.exception("MQTT Broker({:s}:{:s}) connection failed caused by timeout.".format(mqttServer, str(mqttPort)))
    
    # Show error if connection unsuccessful
    def on_connect(self, client, userdata, flag, rc):
        if rc==0:
            logging.info("Connection successful. Ready to Publish")
            print("Connection successful. Ready to Publish")
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
            logging.error("Connection refused - not authorized.")
            print("Connection refused - not authorized.")
    
    def on_publish(self, client, userdata, result):
        pass

    def publish(self, topic, message):
        try:
            self.mqttClient.publish(topic, message, 0)
            #logging.info("Publish Success")
        except:
            logging.exception("Publish Failed")
    
    def publishWithReliable(self, topic, message):
        try:
            self.mqttClient.publish(topic, message, 2)
            print("Published QoS 2 = Topic: {}; Message: {}".format(topic, message))
            #logging.info("Publish QoS 2 Success")
        except:
            logging.exception("Publish QoS 2 Failed")
    
    def on_disconnect(self):
        try:
            print('Reconnecting ....')
            logging.info("Reconnecting ....")
            self.mqttClient.reconnect_delay_set()
        except:
            logging.exception("Failed to reconnect")
        