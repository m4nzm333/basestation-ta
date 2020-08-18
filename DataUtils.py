# Copyright (c) 2020 m4nzm333
# Source code for data conversion
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

# Debug
import random
from datetime import datetime
from Datalog import Datalog


class DataUtils:

    # Convert from Data via Subscriber to String Raw
    # from e.g. 2020-07-14 14:08:43.391928,2020-7-14 14:09:45.394828,34.334232,-5.1381,119.4820,015e topic temperature
    # Format => id,topic,value,lat,long,datetime_sensor,datetime_send, datetime_received
    @staticmethod
    def subscriberPayloadToStringTemp(topic, data):
        delimiter = data.split(',')
        return '{},{},{},{},{},{},{}'.format(delimiter[5], topic, delimiter[2], delimiter[3], delimiter[4], delimiter[0], delimiter[1])
    # With time received

    @staticmethod
    def subscriberPayloadToStringLog(topic, data, timeReceived):
        delimiter = data.split(',')
        return '{},{},{},{},{},{},{},{}'.format(delimiter[5], topic, delimiter[2], delimiter[3], delimiter[4], delimiter[0], delimiter[1], timeReceived)

    # Convert Raw String to Dictionary (JSON like Python)
    # id=abc,temp=xx,long=xxx.xxx,lat=xxx.xxx,timestamp=yyyy-mm-dd HH:MM:ss.sss
    @ staticmethod
    def stringToDictionary(data):
        dicData = {}
        keyVal = data.split(',')
        for splited in keyVal:
            keyValSplited = splited.split('=')
            dicData[keyValSplited[0]] = keyValSplited[1]
        return dicData

    # Check if data is not negative or 0 (data  = dictionary)
    @ staticmethod
    def checkDataValid(sensorName, value):
        # TODO : Fix the filter parameter
        if sensorName == 'temperature' and float(value) <= 0:
            return False
        if sensorName == 'humidity' and float(value) <= 0:
            return False
        if sensorName == 'pressure' and float(value) <= 0:
            return False
        if sensorName == 'co2' and float(value) <= 0:
            return False
        if sensorName == 'co' and float(value) <= 0:
            return False
        if sensorName == 'pm10' and float(value) < 0:
            return False
        # If Valid Return True
        return True

    # Check if data is not negativ or 0 using raw value(string, float)
    @ staticmethod
    def checkDataValidRaw(name, value):
        # TODO : Fix the filter paramter
        switcher = {
            'temperature': False if float(value) <= 0 else True,
            'humidity': False if float(value) <= 0 else True,
            'pressure': False if float(value) <= 0 else True,
            'co2': False if float(value) <= 0 else True,
            'co': False if float(value) <= 0 else True,
            'pm10': False if float(value) < 0 else True  # Bisa bernilai 0
        }
        return switcher.get(name, True)


# Debug
# now = datetime.now()
# 2020-07-14 14:00:45.040310,32.99,1008.11,55.63,130.0058,02:5f
# dataDummy = "abc,{},-5.209925,119.473513,{}".format(
#     str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))
# dataDummy = "{},{},1008.11,55.63,130.0058,02:5f".format(now.strftime(
#     "%Y-%m-%d %H:%M:%S.%f"), str(random.uniform(28.0, 33.5))[:5])
# print(dataDummy)

# dataDummy2 = "abc,{},{}".format(str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))

# print("Debugging : DataUtils.subscriberPayloadToString")
# print(DataUtils.subscriberPayloadToString("temp", dataDummy))

# print("Debugging : DataUtils.stringToDictionary")
# print(DataUtils.che(DataUtils.subscriberPayloadToString("temp", dataDummy2)))

# print("Debugging : DataUtils.checkDataValid")
# print(DataUtils.checkDataValid(DataUtils.stringToDictionary(DataUtils.subscriberPayloadToString("temp", dataDummy))))
