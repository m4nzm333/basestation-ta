# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

from RaspiSubscriber import RaspiSubscriber
from RaspiPublisher import RaspiPublisher
import time

from multiprocessing import Process

# Debug
import random
from datetime import datetime
from Datalog import Datalog

# Main function for subscriber
def subscribe():
    raspiSubscriber = RaspiSubscriber('192.168.1.24', 1883, "Basestation-001")
    print("python main function")

# Main function for publisher
def publish():
    raspiPublisher = RaspiPublisher('192.168.1.7', 1883, "Basestation-002")

    # Still debuging
    while True:
        if raspiPublisher.mqttClient.is_connected:
            now = datetime.now()
            dataDummy = "abc,{},-5.209925,119.473513,{}".format(str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))

            raspiPublisher.publish("temperature", dataDummy)
            time.sleep(1)
        else:
            raspiPublisher = RaspiPublisher('192.168.1.7', 1883, "Basestation-002")
            time.sleep(1)

# Main function for run all function at the same time (Multiprocessing)
def main():
    # Function
    p1 = Process(target=subscribe)
    # p2 = Process(target=publish)
    p1.start()
    # p2.start()
    p1.join()
    # p2.join()

# ----------------
#       MAIN
# ----------------
if __name__ == '__main__':
    main()