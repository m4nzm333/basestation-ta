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
from includes.DataUtils import checkValid, calibrateValue
from includes.SensorBME280 import SensorBME280
from includes.Config import configServerDelay, configServerHostname, configSensor, configServer, configTopic, configMaxNode
from includes.RaspiPublisher import RaspiPublisher
from includes.Queue import queueLength, queueUpdate, queueDelete, queueIsConnected
from gps3 import agps3
import json
from includes.GPS import getLat, getLong
from gpiozero import Button
import RPi.GPIO as GPIO
from includes.CounterData import CounterData
import sys
import socket

# MQTT Client Instance
mqttCSub = mqtt.Client("bs-cd14")
mqttCPub1 = mqtt.Client("cd14-1")
mqttCPub2 = mqtt.Client("cd14-2")

# Check Connection
def checkConnection(host, port=1883):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, port)
    result_of_check = a_socket.connect_ex(location)
    if result_of_check == 0:
        return True
    else:
        return False
# Untuk On Connect Pub
def pubOnConnect(client, userdata, flag, rc):
    print("Pub Connected with result code "+str(rc))
    if rc == 0:
        print("Ready to Publish")
def pubOnDisconnect(client, userdata, rc):
    print("Publihser Disconnected")
# Sub On Connects
def subOnConnect(client, userdata, flag, rc):
    client.subscribe(configTopic())
    print("Sub Connected with result code "+str(rc))
    if rc == 0:
        print("Ready to read data")
# Sub On Messages
def subOnMessage(mosq, obj, msg):
    now = str(datetime.now())
    message = msg.payload.decode('utf-8')
    idSensor, parameter = msg.topic.split('/')
    CounterData.upReceived()
    # Jika Server terkoneksi
    if checkValid(parameter, message):
        # Calibrate Value
        timeSensor, value, lat, lon = message.split(',')
        value = calibrateValue(idSensor, parameter, value)
        message = "{},{},{},{}".format(timeSensor, value, lat, lon)
        logWrite(parameter, now+','+message+','+idSensor)
        if mqttCPub1.is_connected() and configServer() and ((queueLength() ==  configMaxNode() and queueIsConnected(idSensor)) or queueLength() <  configMaxNode()) :
            mqttCPub1.publish(idSensor+'/'+parameter, message)
            queueUpdate(idSensor)
            print("| Published | Node | \33[32m  valid  \033[0m| {} | {}".format(msg.topic, message))
        else:
            tempWrite(parameter, message+","+idSensor)
            print("|  Pending | Node | \33[32m  valid  \033[0m| {} | {}".format(msg.topic, message))
    else:
        print("|  Blocked | Node | \033[91m invalid! \033[0m| {} | {}".format(msg.topic, message))
        CounterData.upBlocked()
        
# Main Function for Subscribe
def subscriber():
    mqttCSub.on_connect = subOnConnect
    mqttCSub.on_message = subOnMessage
    mqttCPub1.on_connect = pubOnConnect
    mqttCPub1.on_disconnect = pubOnDisconnect
    try:
        if configServer() and queueLength() <  configMaxNode():
            print("connecting to Pub1 "+configServerHostname())
            mqttCPub1.connect_async(configServerHostname(), 1883, 30)
            mqttCPub1.loop_start()
        print("Connecting Sub to 127.0.0.1")
        mqttCSub.connect("127.0.0.1", 1883, 30)
        mqttCSub.loop_forever()
    except:
        print("Failed to connect the Sub")

def on_disconnect():
    try:
        mqttCPub2.reconnect_delay_set()
    except:
        pass

def publisher():
    # Main funtion for Publisher with Server at config.json
    if configServer():
        raspiPublisher = RaspiPublisher(configServerHostname(), 1883, "bs-cd14")
        while 1:
            raspiPublisher.mqttClient.loop_start()
            while raspiPublisher.mqttClient.is_connected() and queueLength() <  configMaxNode():
                data = getOldestData()
                for line in data:
                    param, timeSensor, value, lat, lon, idSensor = line.split(",")
                    message = "{},{},{},{},{}".format(timeSensor, value, lat, lon, idSensor)
                    topic = idSensor+'/'+param
                    raspiPublisher.publish(topic, message)
                    CounterData.upSent()
                    print("| Published | Temp | {} | {}".format(topic, message))
                    time.sleep(configServerDelay())
                delOldestData()
                time.sleep(configServerDelay())

def getBME280():
    mqttCPub2.on_connect = pubOnConnect
    mqttCPub2.on_disconnect = pubOnDisconnect
    mqttCPub2.connect(configServerHostname(), 1883, 30)
    while configSensor():
        if True:
            sensorBME280 = SensorBME280()
            now = str(datetime.now())
            valTemp = round(sensorBME280.getTemperature(), 2)
            valHum = round(sensorBME280.getHumidity(), 2)
            valPres = round(sensorBME280.getPressure(), 2)
            valTemp = calibrateValue('cd14', 'temperature', valTemp)
            valHum = calibrateValue('cd14', 'humidity', valHum)
            valPres = calibrateValue('cd14', 'pressure', valPres)
            lat = getLat()
            lon = getLong()
            idSensor = "cd14"
            logWrite("temperature", "{},{},{},{},{},{}".format(now, now, valTemp, lat, lon, idSensor))
            logWrite("humidity", "{},{},{},{},{},{}".format(now, now, valHum, lat, lon, idSensor))
            logWrite("pressure", "{},{},{},{},{},{}".format(now, now, valPres, lat, lon, idSensor))
            mqttCPub2.loop_start()
            if queueLength() < configMaxNode():
                msgTemp = "{},{},{},{}".format(now, valTemp, lat, lon)
                msgHum = "{},{},{},{}".format(now, valHum, lat, lon)
                msgPres = "{},{},{},{}".format(now, valPres, lat, lon) 
                mqttCPub2.publish("cd14/temperature", msgTemp)
                mqttCPub2.publish("cd14/humidity", msgHum)
                mqttCPub2.publish("cd14/pressure", msgPres)
                print("| Published | Internal | \33[32m valid \033[0m| cd14/temperature | " + msgTemp)
                print("| Published | Internal | \33[32m valid \033[0m| cd14/humidity | " + msgHum)
                print("| Published | Internal | \33[32m valid \033[0m| cd14/pressure | " + msgPres)
            else:
                tempWrite("temperature","{},{},{},{},{}".format(now, valTemp, lat, lon, idSensor))
                tempWrite("humidity", "{},{},{},{},{}".format(now, valHum, lat, lon, idSensor))
                tempWrite("pressure", "{},{},{},{},{}".format(now, valPres, lat, lon, idSensor))
        time.sleep(2)

def getLocation():
    # Get currenct location in Longitude and Latitude then save to ./config/location.json
    while True:
        if configSensor() and queueLength() < configMaxNode():
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
        time.sleep(60)


def getDSM():
    # Get Data from Sensor DSM
    while True:
        if configSensor() and queueLength() < configMaxNode():
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
                    tempWrite("pm10", "{},{},{},{},{}".format(now, valPpm, lat, lon, idSensor))
        time.sleep(60)

def queueHandle():
    while True:
        queueDelete()
        time.sleep(5)

def main():
    # Main funtion with multiprocessing
    try:
        # Function
        p1 = Process(target=subscriber)
        p2 = Process(target=publisher)
        p3 = Process(target=getBME280)
        p4 = Process(target=getLocation)
        p5 = Process(target=getDSM)
        p6 = Process(target=queueHandle)
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
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
        p6.terminate()
        p6.kill()


# ----------------
#       MAIN
# ----------------
if __name__ == "__main__":
    main()
