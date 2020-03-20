# Copyright (c) 2020 m4nzm333
# Program for file management
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import os
from datetime import datetime

class Datalog:

    # Make directory for data now
    @staticmethod
    def createDirDate(datetime):
        try:
            os.makedirs("./data/subscriber/{}/{}/{}/{}/{}".format(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute))
        except OSError as e:
            pass
    
    # Output the data (string) into file
    @staticmethod
    def writeStringToFile(data):
        now = datetime.now()
        dirLoc = "./data/subscriber/{}/{}/{}/{}/{}".format(now.year, now.month, now.day, now.hour, now.minute)
        Datalog.createDirDate(now)

        file = open("{}/{}.txt".format(dirLoc, now.strftime("%Y-%m-%d %H:%M:%S")), "a")
        file.write(data+'\n')
        file.close()
    
    # Get oldest file directory location
    @staticmethod
    def getDirLastData():
        try:
            files = os.listdir('./data/subscriber')
            year = os.listdir('./data/subscriber/{}'.format(files[0]))
            year.sort()
            month = os.listdir('./data/subscriber/{}/{}'.format(files[0], year[0]))
            month.sort()
            day = os.listdir('./data/subscriber/{}/{}/{}'.format(files[0], year[0], month[0]))
            day.sort()
            hour = os.listdir('./data/subscriber/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0]))
            hour.sort()
            minute = os.listdir('./data/subscriber/{}/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0], hour[0]))
            minute.sort()

            return './data/subscriber/{}/{}/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0], hour[0], minute[0])
        except:
            return False
    
    # Get array the oldest file content
    @staticmethod
    def getArrayLastData():
        try:
            lastFile = open(Datalog.getDirLastData(), "r")
            return lastFile.readlines()
        except:
            return []