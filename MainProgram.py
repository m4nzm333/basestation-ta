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

# Main function for subscriber
def subscribe():
    raspiSubscriber = RaspiSubscriber('127.0.0.1', 1883, "localSubsciber")

# Main function for publisher
# def publishSensor():
#     led = LED(4)
#     raspiPublisher = RaspiPublisher('127.0.0.1', 1883, "localPublisher")
    
#     while True:
#         if raspiPublisher.mqttClient.is_connected:
#             led.on()
#             now = datetime.now()
#             dataTemperature = "Raspi4-CD14,{:.2f},{}".format(SensorBME280.getTemperature(), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
#             dataHummidity = "Raspi4-CD14,{:.2f},{}".format(SensorBME280.getHummidity(), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
#             dataPressure = "Raspi4-CD14,{:.2f},{}".format(SensorBME280.getPressure(), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
#             raspiPublisher.publish("temperature", dataTemperature)
#             raspiPublisher.publish("hummidity", dataHummidity)
#             raspiPublisher.publish("pressure", dataPressure)
#             time.sleep(0.5)
#             led.off()
#             time.sleep(0.5)
#         else:
#             raspiPublisher = RaspiPublisher('127.0.0.1', 1883, "localPubliser")
#             time.sleep(1)

# Get Data from Local Sensor
def archiveLocalSensor():
    led = LED(4)
    raspiPublisher = RaspiPublisher('127.0.0.1', 1883, "localPublisher")
    sensorBME280 = SensorBME280()
    while True:
        if raspiPublisher.mqttClient.is_connected:
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

# TODO: Make publisher for Server

# Main function for run all function at the same time (Multiprocessing)
def main():
    # Function
    p1 = Process(target=subscribe)
    p2 = Process(target=archiveLocalSensor)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()