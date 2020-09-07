# Copyright (c) 2020 m4nzm333
# Program for file management
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import os
from datetime import datetime
import psutil
import time


class DataTemp:

    # Make directory for data now
    @staticmethod
    def createDirDate(datetime):
        try:
            os.makedirs("./temp/subscriber/{}/{}/{}/{}/{}".format(datetime.year,
                                                                  datetime.month, datetime.day, datetime.hour, datetime.minute))
        except:
            pass

    # Output the data (string) into file
    @staticmethod
    def writeStringToFile(data):
        now = datetime.now()
        dirLoc = "./temp/subscriber/{}/{}/{}/{}/{}".format(
            now.year, now.month, now.day, now.hour, now.minute)
        DataTemp.createDirDate(now)
        file = open("{}/{}.csv".format(dirLoc,
                                       now.strftime("%Y-%m-%d %H:%M:%S")), "a")
        file.write(data+'\n')
        file.close()

    # Get oldest file directory location
    @staticmethod
    def getDirLastData():
        try:
            files = os.listdir('./temp/')
            year = os.listdir('./temp/{}'.format(files[0]))
            year.sort()
            month = os.listdir(
                './temp/{}/{}'.format(files[0], year[0]))
            month.sort()
            day = os.listdir(
                './temp/{}/{}/{}'.format(files[0], year[0], month[0]))
            day.sort()
            hour = os.listdir(
                './temp/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0]))
            hour.sort()
            minute = os.listdir(
                './temp/{}/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0], hour[0]))
            minute.sort()

            return './temp/{}/{}/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0], hour[0], minute[0])
        except:
            return 'False'

    # Get array the oldest file content
    @staticmethod
    def getArrayLastData():
        if DataTemp.getDirLastData() != 'False':
            if DataTemp.checkFileUsed(DataTemp.getDirLastData()) == False:
                lastFile = open(DataTemp.getDirLastData(), "r")
                lastData = lastFile.readlines()
                return lastData
            else:
                return []
        else:
            return []

    # Delete Last File and Empty Directory
    @staticmethod
    def deleteLastData():
        try:
            os.unlink(DataTemp.getDirLastData())
            files = os.listdir('./temp/subscriber')
            year = os.listdir('./temp/subscriber/{}'.format(files[0]))
            year.sort()
            month = os.listdir(
                './temp/subscriber/{}/{}'.format(files[0], year[0]))
            month.sort()
            day = os.listdir(
                './temp/subscriber/{}/{}/{}'.format(files[0], year[0], month[0]))
            day.sort()
            hour = os.listdir(
                './temp/subscriber/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0]))
            hour.sort()
            minute = os.listdir(
                './temp/subscriber/{}/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0], hour[0]))
            minute.sort()

            # Delete directory if Empty and Re-listing directory file
            if len(minute) == 0:
                os.rmdir(
                    './temp/subscriber/{}/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0], hour[0]))
                hour = os.listdir(
                    './temp/subscriber/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0]))
                hour.sort()
            if len(hour) == 0:
                os.rmdir(
                    './temp/subscriber/{}/{}/{}/{}'.format(files[0], year[0], month[0], day[0]))
                day = os.listdir(
                    './temp/subscriber/{}/{}/{}'.format(files[0], year[0], month[0]))
                day.sort()
            if len(day) == 0:
                os.rmdir(
                    './temp/subscriber/{}/{}/{}'.format(files[0], year[0], month[0]))
                month = os.listdir(
                    './temp/subscriber/{}/{}'.format(files[0], year[0]))
                month.sort()
            if len(month) == 0:
                os.rmdir('./temp/subscriber/{}/{}'.format(files[0], year[0]))
                year = os.listdir('./temp/subscriber/{}'.format(files[0]))
                year.sort()
            if len(month) == 0:
                os.rmdir('./temp/subscriber/{}'.format(files[0]))
        except:
            pass

    # Check if current file not in use
    @staticmethod
    def checkFileUsed(fpath):
        for proc in psutil.process_iter():
            try:
                for item in proc.open_files():
                    if fpath == item.path:
                        print(fpath)
                        return True
            except Exception:
                pass
        return False

# fullPath = '/home/pi/Documents/basestation-ta/data/subscriber/2020/3/25/23/43/2020-03-25 23:43:42.txt'
# fileOpen = open(fullPath, 'r')
# print(DataTemp.checkFileUsed(fullPath))
# fileOpen.close()
# fileOpen.close()
# print(DataTemp.checkFileUsed(fullPath))
