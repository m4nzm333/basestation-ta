# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

from RaspiSubscriber import RaspiSubscriber
from RaspiPublisher import RaspiPublisher
import time
from multiprocessing import Process
# from SensorBME280 import SensorBME280
from datetime import datetime
from Datalog import Datalog
from DataUtils import DataUtils
from gpiozero import LED
import sys
# from api.api import app

# Main function for subscriber
def subscribe():
    RaspiSubscriber('192.168.137.1', 1883, "bs-cd14")

# Main function for publisher
def publishTempToServer():
    raspiPublisher = RaspiPublisher('192.168.137.1', 1883, "bs-cd14")
    while 1:
        raspiPublisher.mqttClient.loop_start()
        while raspiPublisher.mqttClient.is_connected():
            lastArray = Datalog.getArrayLastData()
            # Loop foreach data in Array
            for data in lastArray:
                dicData = DataUtils.getDicToPublish(data)
                raspiPublisher.publish(dicData['topic'], dicData['message'])
                time.sleep(0.5)
            Datalog.deleteLastData()
            time.sleep(0.1)

# Get Data from Local Sensor
# def archiveLocalSensor():
#     # TODO: ganti data row untuk masing-masing sensor
#     led = LED(4)
#     sensorBME280 = SensorBME280()
#     while True:
#         led.on()
#         now = datetime.now()
#         valTemperature = sensorBME280.getTemperature()
#         valHummitidy = sensorBME280.getHummidity()
#         valPressure = sensorBME280.getPressure()
#         # Check Data Valid
#         if DataUtils.checkDataValidRaw('temperature', valTemperature):          
#             dataTemperature = "id=Raspi4-CD14,temperature={:.2f},timestamp={}".format(valTemperature, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
#             Datalog.writeStringToFile(dataTemperature)
#         if DataUtils.checkDataValidRaw('hummidity', valHummitidy):
#             dataHummidity = "id=Raspi4-CD14,hummidity={:.2f},timestamp={}".format(valHummitidy, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
#             Datalog.writeStringToFile(dataHummidity)
#         if DataUtils.checkDataValidRaw('pressure', valPressure):
#             dataPressure = "id=Raspi4-CD14,pressure={:.2f},timestamp={}".format(valPressure, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
#             Datalog.writeStringToFile(dataPressure)
#         time.sleep(0.5)
#         led.off()
#         time.sleep(4.5)

# Start API HTTP Server
# def startApiServer():
#     app.run('0.0.0.0', 8000)

# Main function for run all function at the same time (Multiprocessing)
def main():
    try:
        # Function
        p1 = Process(target=subscribe)
        p1.start()
        p1.join()
        # p2 = Process(target=archiveLocalSensor)
        # p2.start()
        # p2.join()
        # p3 = Process(target=publishTempToServer)
        # p3.start()
        # p3.join()
        # p4 = Process(target=startApiServer)
        # p4.start()
        # p4.join()
    except KeyboardInterrupt:
        p1.terminate()
        p1.kill()
        # p2.terminate()
        # p2.kill()
        # p3.terminate()
        # p3.kill()
        # p4.terminate()
        # p3.kill()

# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()