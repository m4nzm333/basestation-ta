# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import paho.mqtt.client as mqtt
import time
from multiprocessing import Process
from datetime import datetime

from includes.Datalog import logWrite
from includes.DataTemp import tempWrite, getOldestData, delOldestData
from includes.DataUtils import checkValid
from includes.SqlMonitor import sqlWrite, sqlUpdate
from includes.RaspiPublisher import RaspiPublisher
from includes.SensorBME280 import SensorBME280
from includes.Config import configServerDelay, configServerHostname, configSensor, configServer, configTopic
from gps3 import agps3
import json
from includes.GPS import getLat, getLong
from gpiozero import Button
import RPi.GPIO as GPIO
from includes.CounterData import CounterData
import sys

# MQTT Client Instance
mqttCSub = mqtt.Client("bs-cd14")
mqttCSubState = False
mqttCPub1 = mqtt.Client("cd14-1")
mqttCPub1State = False
mqttCPub2 = mqtt.Client("cd14-2")
mqttCPub2State = False

# Untuk On Connect Pub
def pubOnConnect(client, userdata, flag, rc):
    global mqttCPub1State
    mqttCPub1State = True
    print("Pub Connected with result code "+str(rc))
    print("Ready to Publish")
def pubOnDisconnect(client, userdata, rc):
    global mqttCPub1State
    mqttCPub1State =  False
    print("disconnected")
# Sub On Connects
def subOnConnect(client, userdata, flag, rc):
    client.subscribe(configTopic())
    print("Sub Connected with result code "+str(rc))
    print("Ready to read data")
    global mqttCSubState
    mqttCSubState =  True
# Sub On Messages
def subOnMessage(mosq, obj, msg):
    now = str(datetime.now())
    message = msg.payload.decode('utf-8')
    idSensor, parameter = msg.topic.split('/')
    CounterData.upReceived()
    logWrite(parameter, now+','+message+','+idSensor)
    # Jika Server terkoneksi
    if checkValid(parameter, message):
        if mqttCPub1State:
            mqttCPub1.publish(idSensor+'/'+parameter, message)
        else:
            tempWrite(parameter, message)
            print("|  Pending |\33[32m  valid  \033[0m| {} | {}".format(msg.topic, message))
    else:
        print("|  Blocked |\033[91m invalid! \033[0m| {} | {}".format(msg.topic, message))
        CounterData.upBlocked()
# Main Function for Subscribe
def subscribe():
    mqttCSub.on_connect = subOnConnect
    mqttCSub.on_message = subOnMessage
    mqttCPub1.on_connect = pubOnConnect
    mqttCPub1.on_disconnect = pubOnDisconnect
    try:
        print("Connecting Sub to 127.0.0.1")
        mqttCSub.connect("127.0.0.1", 1883, 30)
        mqttCSub.loop_forever()
        # Pub
    except:
        print("Failed to connect the Sub")
    # # Main funtion for Subscriber with Server to listen at local broker
    # RaspiSubscriber("127.0.0.1", 1883, "bs-cd14")

def publishTempToServer():
    print('none')
    # Main funtion for Publisher with Server at config.json
    # if configServer():
    #     raspiPublisher = RaspiPublisher(configServerHostname(), 1883, "bs-cd14")
    #     while 1:
    #         raspiPublisher.mqttClient.loop_start()
    #         while raspiPublisher.mqttClient.is_connected():
    #             data = getOldestData()
    #             delOldestData()
    #             for line in data:
    #                 topic, timeSensor, value, lat, lon, idSensor = line.split(",")
    #                 message = "{},{},{},{}".format(timeSensor, value, lat, lon)
    #                 raspiPublisher.publish(idSensor+'/'+topic, message)
    #                 CounterData.upSent()
    #                 print("|  Publish   |\33[32m  valid  \033[0m| {} | {}".format(topic, message))
    #                 time.sleep(configServerDelay())
    #             time.sleep(configServerDelay())
    #         raspiPublisher.mqttClient.loop_stop()

def getBME280():
    # Get Data From BME280
    if configSensor():
        sensorBME280 = SensorBME280()
        while True:
            now = str(datetime.now())
            valTemp = round(sensorBME280.getTemperature(), 2)
            valHum = round(sensorBME280.getHumidity(), 2)
            valPres = round(sensorBME280.getPressure(), 2)

            lat = getLat()
            lon = getLong()
            idSensor = "cd14"
            # Write to Log
            logWrite("temperature", "{},{},{},{},{}".format(now,  valTemp, lat, lon, idSensor))
            logWrite("humidity", "{},{},{},{},{}".format(now, valHum, lat, lon, idSensor))
            logWrite("pressure", "{},{},{},{},{}".format(now, valHum, lat, lon, idSensor))
            # Write to Temp
            if valTemp != 0:
                tempWrite("temperature", "{},{},{},{},{},{}".format(now, now, valTemp, lat, lon, idSensor),)
            if valHum != 0:
                tempWrite("humidity", "{},{},{},{},{},{}".format(now, now, valHum, lat, lon, idSensor))
            if valPres != 0 and valPres >= 900:
                tempWrite("pressure", "{},{},{},{},{},{}".format(now, now, valPres, lat, lon, idSensor))
            time.sleep(60)

def getLocation():
    # Get currenct location in Longitude and Latitude then save to ./config/location.json
    if configSensor():
        try:
            gps_socket = agps3.GPSDSocket()
            data_stream = agps3.DataStream()
            gps_socket.connect()
            gps_socket.watch()
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    lon = None
                    lat = None
                    if data_stream.lon != "n/a":
                        lon = round(float(data_stream.lon), 6)
                        lat = round(float(data_stream.lat), 6)
                    file = open("config/location.json", "w+")
                    stringLocation = {
                        "lat": str(lat),
                        "long": str(lon),
                        "update": str(datetime.now()),
                    }
                    file.write(json.dumps(stringLocation, separators=(",", ":"), sort_keys=True, indent=4))
                    file.close()
                time.sleep(5)
        except:
            pass


def getDSM():
    # Get Data from Sensor DSM
    if configSensor():
        button = Button(17)
        while True:
            x1 = 2500
            y1 = 5
            x2 = 12500
            y2 = 25
            m = (y2 - y1) / (x2 - x1)  # Gradien
            start = int(time.time() * 1000000)
            lowDuration = 0
            while True:
                dif = int(time.time() * 1000000)
                if button.is_pressed:
                    lowDuration += 100
                if (dif - start) >= 30000000:  # 30 sec
                    break
                time.sleep(0.0001)
            lowRatio = (lowDuration / 30000000) * 100
            xPPM = ((lowRatio - 5) / m) + 2500
            valPpm = round(xPPM, 0)

            now = str(datetime.now())
            idSensor = 'cd14'
            lat = getLat()
            lon = getLong()

            # Write Log
            logWrite("pm10", "{},{},{},{},{}".format(now, valPpm, lat, lon, idSensor))
            if valPpm != 0:
                tempWrite("pm10", "{},{},{},{},{}".format(now, valPpm, lat, lon, idSensor),)


def main():
    # Main funtion with multiprocessing
    try:
        # Function
        p1 = Process(target=subscribe)
        p2 = Process(target=publishTempToServer)
        p3 = Process(target=getBME280)
        p4 = Process(target=getLocation)
        p5 = Process(target=getDSM)
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
    except KeyboardInterrupt:
        p1.terminate()
        p1.kill()
        p2.terminate()
        p2.kill()
        p3.terminate()
        p3.kill()
        p4.terminate()
        p4.kill()
        p5.terminate()
        p5.kill()


# ----------------
#       MAIN
# ----------------
if __name__ == "__main__":
    main()
