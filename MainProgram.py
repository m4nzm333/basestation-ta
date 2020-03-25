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
from DataUtils import DataUtils
from gpiozero import LED
import sys

# Main function for subscriber
def subscribe():
    raspiSubscriber = RaspiSubscriber('127.0.0.1', 1883, "localSubsciber")

# Main function for publisher
def publishTempToServer():
    raspiPublisher = RaspiPublisher('192.168.1.7', 1883, "Omaera")
    # Exception for not passing False on loop
    #raspiPublisher.publishWithReliable('data', 'this is data')
    # while True:
    #     try:    
    #         lastArray = Datalog.getArrayLastData()
    #         # Loop foreach data in Array
    #         for data in lastArray:
    #             # Check if connection Establish
    #             # while raspiPublisher.mqttClient.is_connected == False:
    #             #     raspiPublisher.mqttClient.disconnect()
    #             #     raspiPublisher = RaspiPublisher('192.168.1.7', 1883, "Raspi4-C4")
    #             raspiPublisher.publishWithReliable('data', data)
    #             time.sleep(0.5)
    #         Datalog.deleteLastData()
    #         time.sleep(0.5)
    #     # Program wont close even using Ctrl + C to Interupt
    #     # So I'm made a Spesific Exception
    #     except KeyboardInterrupt:
    #         sys.exit()
    #     except:
    #         pass

# Get Data from Local Sensor
def archiveLocalSensor():
    led = LED(4)
    sensorBME280 = SensorBME280()
    while True:
        led.on()
        now = datetime.now()
        valTemperature = sensorBME280.getTemperature()
        valHummitidy = sensorBME280.getHummidity()
        valPressure = sensorBME280.getPressure()
        # Check Data Valid
        if DataUtils.checkDataValidRaw('temperature', valTemperature):          
            dataTemperature = "id=Raspi4-CD14,temperature={:.2f},timestamp={}".format(valTemperature, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
            Datalog.writeStringToFile(dataTemperature)
        if DataUtils.checkDataValidRaw('hummidity', valHummitidy):
            dataHummidity = "id=Raspi4-CD14,hummidity={:.2f},timestamp={}".format(valHummitidy, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
            Datalog.writeStringToFile(dataHummidity)
        if DataUtils.checkDataValidRaw('pressure', valPressure):
            dataPressure = "id=Raspi4-CD14,pressure={:.2f},timestamp={}".format(valPressure, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
            Datalog.writeStringToFile(dataPressure)
        time.sleep(0.5)
        led.off()
        time.sleep(4.5)

# Main function for run all function at the same time (Multiprocessing)
def main():
    # Function
    #p1 = Process(target=subscribe)
    #p2 = Process(target=archiveLocalSensor)
    p3 = Process(target=publishTempToServer)
    #p1.start()
    #p2.start()
    p3.start()
    #p1.join()
    #p2.join()
    p3.join()

# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()