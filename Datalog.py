# Copyright (c) 2020 m4nzm333
# Program for file management
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import os
from datetime import datetime
import psutil
import time


class Datalog:

    # Make directory for data now
    @staticmethod
    def createDirDate(datetime):
        try:
            os.makedirs("./log/{}/{}/{}/{}/{}".format(datetime.year,
                                                                  datetime.month, datetime.day, datetime.hour, datetime.minute))
        except:
            pass

    # Output the data (string) into file
    @staticmethod
    def writeStringToFile(data, datetimesensor):
        timeSensor = datetime.strptime(datetimesensor, "%Y-%m-%d %H:%M:%S.%f")
        dirLoc = "./log/{}/{}/{}/{}/{}".format(
            timeSensor.year, timeSensor.month, timeSensor.day, timeSensor.hour, timeSensor.minute)
        Datalog.createDirDate(timeSensor)
        file = open("{}/{}.csv".format(dirLoc,
                                       timeSensor.strftime("%Y-%m-%d %H:%M:%S")), "a")
        file.write(data+'\n')
        file.close()

# fullPath = '/home/pi/Documents/basestation-ta/data/subscriber/2020/3/25/23/43/2020-03-25 23:43:42.txt'
# fileOpen = open(fullPath, 'r')
# print(Datalog.checkFileUsed(fullPath))
# fileOpen.close()
# fileOpen.close()
# print(Datalog.checkFileUsed(fullPath))
