# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com


import time
from multiprocessing import Process
from datetime import datetime

from includes.Datalog import Datalog
from includes.DataTemp import DataTemp
from includes.DataUtils import DataUtils
from includes.SqlMonitor import SqlMonitor
from includes.RaspiSubscriber import RaspiSubscriber
from includes.RaspiPublisher import RaspiPublisher
from includes.SensorBME280 import SensorBME280
from includes.CPUMonitor import CPUMonitor
from gps3 import agps3
import json
from includes.GPS import getLat, getLong
from gpiozero import Button
import RPi.GPIO as GPIO
# from gpiozero import LED
import sys
# from api.api import app

# Main function for subscriber


def subscribe():
    RaspiSubscriber('127.0.0.1', 1883, "bs-cd14")

# Main function for publisher


def publishTempToServer():
    # Server : 10.0.12.127
    raspiPublisher = RaspiPublisher('182.23.82.22', 1883, "bs-cd14")
    while 1:
        raspiPublisher.mqttClient.loop_start()
        while raspiPublisher.mqttClient.is_connected():
            lastArray = DataTemp.getArrayLastData()
            # Loop foreach data in Array
            for data in lastArray:
                idSensor, topic, value, lat, longit, timeSensor, timeReceived = data.split(
                    ',')
                # Filter if Valid
                if DataUtils.checkDataValid(topic, value):
                    raspiPublisher.publish(topic, '{},{},{},{},{}'.format(
                        timeSensor, value, lat, longit, idSensor))
                    SqlMonitor.sqlUpdate(idSensor, timeSensor, topic, str(datetime.now()))
                time.sleep(0.4)
            DataTemp.deleteLastData()
            time.sleep(0.1)
# TODO: Waiting for Confirmation from Server Broker

# Get Data From BME280


def getBME280():
    # TODO: ganti data row untuk masing-masing sensor
    sensorBME280 = SensorBME280()
    while True:
        now = datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        valTemp = round(sensorBME280.getTemperature(), 2)
        valHum = round(sensorBME280.getHumidity(), 2)
        valPres = round(sensorBME280.getPressure(), 2)

        lat = getLat()
        longit = getLong()

        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'temperature', valTemp, lat, longit, nowString, ''), nowString)
        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'humidity', valHum, lat, longit, nowString, ''), nowString)
        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'pressure', valPres, lat, longit, nowString, ''), nowString)
        # Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
        #     'cd14', 'altitude', valTemp, '', '', nowString, ''), nowString)

        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'temperature', valTemp, lat, longit, nowString, ''))
        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'humidity', valHum, lat, longit, nowString, ''))
        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'pressure', valPres, lat, longit, nowString, ''))
        # DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
        #     'cd14', 'temperature', valTemp, '', '', nowString, ''))
        SqlMonitor.sqlWrite('temperature', "{},{},{},{},{},{}".format(
            nowString, nowString, valTemp, lat, longit, 'cd14'), nowString)
        SqlMonitor.sqlWrite('humidity', "{},{},{},{},{},{}".format(
            nowString, nowString, valHum, lat, longit, 'cd14'), nowString)
        SqlMonitor.sqlWrite('pressure', "{},{},{},{},{},{}".format(
            nowString, nowString, valPres, lat, longit, 'cd14'), nowString)

        time.sleep(60)

# GPS Conf


def getLocation():
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
                # print('Longitude = ', str(lon))
                # print('Latitude = ', str(lat))
                # print(str(datetime.now()))
                file = open("config/location.json", "w+")
                stringLocation = {
                    "lat": str(lat),
                    "long": str(lon),
                    "update": str(datetime.now())
                }
                file.write(json.dumps(stringLocation, separators=(',', ':')))
                file.close()
            time.sleep(5)
    except:
        pass

def getDSM():
    button = Button(17)
    while True:
        x1 = 2500
        y1 = 5
        x2 = 12500
        y2 = 25
        m = (y2 - y1) / (x2 - x1) # Gradien
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

        nowString = str(datetime.now())

        lat = getLat()
        longit = getLong()

        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
                'cd14', 'ppm10', valPpm, lat, longit, nowString, ''), nowString)
        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
                'cd14', 'ppm10', valPpm, lat, longit, nowString, ''))
        SqlMonitor.sqlWrite('ppm10', "{},{},{},{},{},{}".format(
                nowString, nowString, valPpm, lat, longit, 'cd14'), nowString)

def getCPU():
    while True:
        CPUMonitor.sqlWrite()
        time.sleep(1)

# Start API HTTP Server
# def startApiServer():
#     app.run('0.0.0.0', 8000)

# Main function for run all function at the same time (Multiprocessing)


def main():
    try:
        # Function
        p1 = Process(target=subscribe)
        # p2 = Process(target=getBME280)
        p3 = Process(target=publishTempToServer)
        # p4 = Process(target=getLocation)
        # p5 = Process(target=getDSM)
        p6 = Process(target=getCPU)
        p1.start()
        # p2.start()
        p3.start()
        # p4.start()
        # p5.start()
        p6.start()
        p1.join()
        # p2.join()
        p3.join()
        # p4.join()
        # p5.join()
        p6.join()
    except KeyboardInterrupt:
        p1.terminate()
        p1.kill()
        # p2.terminate()
        # p2.kill()
        p3.terminate()
        p3.kill()
        # p4.terminate()
        # p4.kill()
        # p5.terminate()
        # p5.kill()
        p6.terminate()
        p6.kill()


# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()
