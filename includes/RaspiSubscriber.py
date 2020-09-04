# Copyright (c) 2020 m4nzm333
# Source code for receive data from Sensor Node
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import paho.mqtt.client as mqtt
from datetime import datetime
import logging
from includes.Datalog import Datalog
from includes.DataTemp import DataTemp
from includes.SqlMonitor import SqlMonitor
from includes.CounterData import CounterData
from includes.DataUtils import DataUtils
from includes.CounterData import CounterData

# Class for Raspberry Subscriber


class RaspiSubscriber:

    # Instance Attribute
    def __init__(self, mqttServer, mqttPort, clientName):
        logging.basicConfig(filename='./log/subscriber.log',
                            format='%(asctime)s %(message)s', level=logging.DEBUG)
        keepAliveInterval = 30
        mqttTopic = [("temperature", 0), ("pressure", 0), ("altitude", 0),
                     ("humidity", 0), ("so", 0), ("co", 0), ("co2", 0), ("pm10", 0)]

        mqttClient = mqtt.Client(clientName)

        # Assign Event Callbacks
        mqttClient.on_message = self.on_message
        mqttClient.on_subscribe = self.on_subscribe
        mqttClient.on_connect = self.on_connect

        # Connect
        logging.info("Connecting to MQTT Broker({:s}:{:s}).".format(
            mqttServer, str(mqttPort)))
        print("Connecting to MQTT Broker({:s}:{:s}).".format(
            mqttServer, str(mqttPort)))
        try:
            mqttClient.connect(mqttServer, mqttPort, keepAliveInterval)
        except:
            logging.exception("MQTT Broker({:s}:{:s}) connection failed caused by timeout.".format(
                mqttServer, str(mqttPort)))
        mqttClient.subscribe(mqttTopic)
        # Continue the network loop
        mqttClient.loop_forever()

    # Read Data Function
    def on_message(self, mosq, obj, msg):
        nowString = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        sensorMsg = msg.payload.decode('utf-8')

        CounterData.upReceived()
        try:
            print("| Received |\33[34m  pending  \033[0m| {} | {}".format(
                msg.topic, sensorMsg))
            Datalog.writeStringToFile(DataUtils.subscriberPayloadToStringLog(
                msg.topic, sensorMsg, nowString), sensorMsg.split(',')[0])
            splitter = sensorMsg.split(',')
            if len(splitter) == 6 and splitter[0] != '2000-00-00 08:00:00.484000':
                DataTemp.writeStringToFile(
                    DataUtils.subscriberPayloadToStringTemp(msg.topic, sensorMsg))
                SqlMonitor.sqlWrite(msg.topic, sensorMsg, nowString)
            else:
                print("| Received |\033[91m invalid! \033[0m| {} | {}".format(
                    msg.topic, sensorMsg))
                CounterData.upBlocked()

        except:
            print("| Received |\033[91m invalid! \033[0m| {} | {}".format(
                msg.topic, sensorMsg))
            CounterData.upBlocked()
            pass

    # Show error if connection unsuccessful

    def on_connect(self, client, userdata, flag, rc):
        if rc == 0:
            logging.info("Connection successful. Waiting for data.")
            print("Connection successful. Waiting for data.")
        if rc == 1:
            logging.error("Connection refused - incorrect protocol version.")
            print("Connection refused - incorrect protocol version")
        if rc == 2:
            logging.error("Connection refused - invalid client identifier.")
            print("Connection refused - invalid client identifier.")
        if rc == 3:
            logging.error("Connection refused - server unavailable.")
            print("Connection refused - server unavailable.")
        if rc == 4:
            logging.error("Connection refused - not authorised.")
            print("Connection refused - not authorised.")
        print("|---Action---|----Status----|----Topic----|----data")

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        logging.info('Subscribe to {:s}'.format(str(mosq.topic)))
        print('Subscribe to {:s}'.format(str(mosq.topic)))
