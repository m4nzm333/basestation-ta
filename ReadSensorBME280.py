# Copyright (c) 2020 m4nzm333
# Source code for read sensor data from BME280 Module
#   * Temperature
#   * Pressure
#   * Hummidity
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import smbus2
import bme280

# Address I2C
port = 1
address = 0x76
bus = smbus2.SMBus(port)

import paho.mqtt.client as mqtt
import datetime as datetime
from time import sleep
# For testcase, delete later
from random import randint

# Get Data from Sensor
calibration_params = bme280.load_calibration_params(bus, address)

def getTemperature():
    data = bme280.sample(bus, address, calibration_params)
    return data.temperature

def getPressure():
    data = bme280.sample(bus, address, calibration_params)
    return data.pressure

def getHummidity():
    data = bme280.sample(bus, address, calibration_params)
    return data.humidity


# MQTT Setting
MQTT_Broker = "192.168.1.5"
MQTT_Port = 1883
Keep_Alive_Interval = 45

# Client object
mqttc = mqtt.Client("Basestation-0002")

# Publish Callback
def on_publish(client, userdata, result):
    pass

# Try to connect callback
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

# Published data should be from data log
# data sample id=123456;temp=10;timestamp=2019-11-15-06:04:22.123123

# TODO : Data log reader algorithm

def main():
    # Assign Event Callbacks]
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect

    # Connect
    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

    # Publish (Topic, Data)
    topicList = ["temperature", "pressure", "hummidity"]
    while 1:
        sleep(1)
        print("id=basestation1;"+ topicList[0] +"="+ str(getTemperature()) +";timestamp="+datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
        mqttc.publish(topicList[0],"id=basestation1;"+ topicList[0] +"="+ str(getTemperature()) +";timestamp="+datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
        mqttc.publish(topicList[1],"id=basestation1;"+ topicList[1] +"="+ str(getPressure()) +";timestamp="+datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
        mqttc.publish(topicList[2],"id=basestation1;"+ topicList[2] +"="+ str(getHummidity()) +";timestamp="+datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
