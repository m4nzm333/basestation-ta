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

# Debug
import random
from datetime import datetime
from Datalog import Datalog

# Main function for subscriber
def subscribe():
    raspiSubscriber = RaspiSubscriber('127.0.0.1', 1883, "localSubsciber")

# Main function for publisher
def publish():
    raspiPublisher = RaspiPublisher('127.0.0.1', 1883, "localPublisher")

    # Still debuging
    while True:
        if raspiPublisher.mqttClient.is_connected:
            now = datetime.now()
            dataTemperature = "Raspi4-CD14,{:.2f},{}".format(SensorBME280.getTemperature(), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
            dataHummidity = "Raspi4-CD14,{:.2f},{}".format(SensorBME280.getHummidity(), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
            dataPressure = "Raspi4-CD14,{:.2f},{}".format(SensorBME280.getPressure(), now.strftime("%Y-%m-%d %H:%M:%S.%f"))
            raspiPublisher.publish("temperature", dataTemperature)
            raspiPublisher.publish("hummidity", dataHummidity)
            raspiPublisher.publish("pressure", dataPressure)
            time.sleep(1)
        else:
            raspiPublisher = RaspiPublisher('127.0.0.1', 1883, "localPubliser")
            time.sleep(1)

# Main function for run all function at the same time (Multiprocessing)
def main():
    # Function
    p1 = Process(target=subscribe)
    p2 = Process(target=publish)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()