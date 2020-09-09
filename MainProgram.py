# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import time
from multiprocessing import Process
from datetime import datetime

from includes.Datalog import logWrite
from includes.DataTemp import tempWrite, getOldestData, delOldestData
from includes.DataUtils import checkValid
from includes.SqlMonitor import sqlWrite, sqlUpdate
from includes.RaspiSubscriber import RaspiSubscriber
from includes.RaspiPublisher import RaspiPublisher
from includes.SensorBME280 import SensorBME280
from includes.Config import (
    configServerDelay,
    configServerHostname,
    configSensor,
    configServer,
)
from gps3 import agps3
import json
from includes.GPS import getLat, getLong
from gpiozero import Button
import RPi.GPIO as GPIO
from includes.CounterData import CounterData
import sys


def subscribe():
    # Main funtion for Subscriber with Server to listen at local broker
    RaspiSubscriber("127.0.0.1", 1883, "bs-cd14")


def publishTempToServer():
    # Main funtion for Publisher with Server at config.json
    if configServer():
        raspiPublisher = RaspiPublisher(
            configServerHostname(), 1883, "bs-cd14")
        while 1:
            raspiPublisher.mqttClient.loop_start()
            while raspiPublisher.mqttClient.is_connected():
                data = getOldestData()
                for line in data:
                    topic, timeSensor, sendTime, value, lat, lon, idSensor = line.split(
                        ",")
                    message = "{},{},{},{},{}".format(
                        timeSensor, value, lat, lon, idSensor)
                    raspiPublisher.publish(topic, message)
                    CounterData.upSent()
                    now = str(datetime.now())
                    sqlUpdate(idSensor, timeSensor, topic, now)
                    print("|  Publish   |\33[32m  valid    \033[0m| {} | {}".format(
                        topic, message))
                    time.sleep(configServerDelay())
                delOldestData()
                time.sleep(configServerDelay())


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
            logWrite("temperature", "{},{},{},{},{},{}".format(
                now, now, valTemp, lat, lon, idSensor))
            logWrite("humidity", "{},{},{},{},{},{}".format(
                now, now, valHum, lat, lon, idSensor))
            logWrite("pressure", "{},{},{},{},{},{}".format(
                now, now, valHum, lat, lon, idSensor))
            # Write to SQL
            sqlWrite("temperature", "{},{},{},{},{},{}".format(
                now, now, valTemp, lat, lon, "cd14"), now,)
            sqlWrite("humidity", "{},{},{},{},{},{}".format(
                now, now, valHum, lat, lon, "cd14"), now)
            sqlWrite("pressure", "{},{},{},{},{},{}".format(
                now, now, valPres, lat, lon, idSensor), now)
            # Write to Temp
            if valTemp != 0:
                tempWrite("temperature", "{},{},{},{},{},{}".format(
                    now, now, valTemp, lat, lon, idSensor),)
            if valHum != 0:
                tempWrite("humidity", "{},{},{},{},{},{}".format(
                    now, now, valHum, lat, lon, idSensor))
            if valPres != 0:
                tempWrite("pressure", "{},{},{},{},{},{}".format(
                    now, now, valPres, lat, lon, idSensor))

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
                    file.write(json.dumps(stringLocation, separators=(
                        ",", ":"), sort_keys=True, indent=4))
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
                    # print("Button is not pressed")
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
            logWrite("pm10", "{},{},{},{},{},{}".format(
                now, now, valPpm, lat, lon, idSensor))
            # Write to SQL
            sqlWrite("pm10", "{},{},{},{},{},{}".format(
                now, now, valPpm, lat, lon, "cd14"), now,)
            if valPpm != 0:
                tempWrite("pm10", "{},{},{},{},{},{}".format(
                    now, now, valPpm, lat, lon, idSensor),)


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
