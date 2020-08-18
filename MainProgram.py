# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

from RaspiSubscriber import RaspiSubscriber
from RaspiPublisher import RaspiPublisher
import time
from multiprocessing import Process
from SensorBME280 import SensorBME280
from datetime import datetime
from Datalog import Datalog
from DataTemp import DataTemp
from DataUtils import DataUtils
from SqlMonitor import SqlMonitor
# from gpiozero import LED
import sys
# from api.api import app

# Main function for subscriber
def subscribe():
    RaspiSubscriber('127.0.0.1', 1883, "bs-cd14")

# Main function for publisher
def publishTempToServer():
    raspiPublisher = RaspiPublisher('192.168.1.2', 1883, "bs-cd14")
    while 1:
        raspiPublisher.mqttClient.loop_start()
        while raspiPublisher.mqttClient.is_connected():
            lastArray = DataTemp.getArrayLastData()
            # Loop foreach data in Array
            for data in lastArray:
                print(data)
                idSensor, topic, value, lat, longit, timeSensor, timeReceived = data.split(
                    ',')
                # Filter if Valid
                if DataUtils.checkDataValid(topic, value):
                    raspiPublisher.publish(topic, '{},{},{},{},{}'.format(
                        timeSensor, value, lat, longit, idSensor))

                time.sleep(0.5)
            DataTemp.deleteLastData()
            time.sleep(0.1)
# TODO: Waiting for Confirmation from Server Broker

# Get Data from BME280
def getBME280():
    # TODO: ganti data row untuk masing-masing sensor
    sensorBME280 = SensorBME280()
    while True:
        now = datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        valTemp = sensorBME280.getTemperature()
        valHum = sensorBME280.getHumidity()
        valPres = sensorBME280.getPressure()

        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'temperature', valTemp, '', '', nowString, ''), nowString)
        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'humidity', valHum, '', '', nowString, ''), nowString)
        Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'pressure', valPres, '', '', nowString, ''), nowString)
        # Datalog.writeStringToFile("{},{},{},{},{},{},{}".format(
        #     'cd14', 'altitude', valTemp, '', '', nowString, ''), nowString)

        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'temperature', valTemp, '', '', nowString, ''))
        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'humidity', valHum, '', '', nowString, ''))
        DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
            'cd14', 'pressure', valPres, '', '', nowString, ''))
        # DataTemp.writeStringToFile("{},{},{},{},{},{},{}".format(
        #     'cd14', 'temperature', valTemp, '', '', nowString, ''))
        SqlMonitor.sqlWrite('temperature', "{},{},{},{},{},{}".format(
            nowString, nowString, valTemp, '', '', 'cd14'), nowString)
        SqlMonitor.sqlWrite('humidity', "{},{},{},{},{},{}".format(
            nowString, nowString, valHum, '', '', 'cd14'), nowString)
        SqlMonitor.sqlWrite('pressure', "{},{},{},{},{},{}".format(
            nowString, nowString, valPres, '', '', 'cd14'), nowString)

        time.sleep(10)

# Start API HTTP Server
# def startApiServer():
#     app.run('0.0.0.0', 8000)

# Main function for run all function at the same time (Multiprocessing)


def main():
    try:
        # Function
        p1 = Process(target=subscribe)
        p2 = Process(target=getBME280)
        p3 = Process(target=publishTempToServer)
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
        # p4 = Process(target=startApiServer)
        # p4.start()
        # p4.join()
    except KeyboardInterrupt:
        p1.terminate()
        p1.kill()
        p2.terminate()
        p2.kill()
        p3.terminate()
        p3.kill()
        # p4.terminate()
        # p3.kill()

# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()
