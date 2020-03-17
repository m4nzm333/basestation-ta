# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

from RaspiSubscriber import RaspiSubscriber
from RaspiPublisher import RaspiPublisher
import time

def main():
    raspiSubscriber = RaspiSubscriber('192.168.1.7', 1883, "Basestation-001")
    print("python main function")

def publish():
    raspiPublisher = RaspiPublisher('192.168.1.7', 1883, "Basestation-002")
    while True:
        print("Python Raspi Publisher Execute")
        raspiPublisher.publish("temp", "This is message")
        time.sleep(5)
    

if __name__ == '__main__':
    publish()

