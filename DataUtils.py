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
    # abc,xx,xxx.xxx,xxx.xxx,yyyy-mm-dd HH:MM:ss.sss
    # to
    # id=abc,temp=xx,long=xxx.xxx,lat=xxx.xxx,timestamp=yyyy-mm-dd HH:MM:ss.sss
    @staticmethod
    def subscriberPayloadToString(topic, data):
        delimiter = data.split(',')
        # Check if 3rd data is timestamp
        try:
            datetime.strptime(delimiter[2], "%Y-%m-%d %H:%M:%S.%f")
            return "id={},{}={},timestamp={}".format(delimiter[0], topic, delimiter[1], delimiter[2])
        except:
            return "id={},{}={},long={},lat={},timestamo={}".format(delimiter[0], topic, delimiter[1], delimiter[2], delimiter[3], delimiter[4])
    
    # Convert Raw String to Dictionary (JSON like Python)
    # id=abc,temp=xx,long=xxx.xxx,lat=xxx.xxx,timestamp=yyyy-mm-dd HH:MM:ss.sss
    @staticmethod
    def stringToDictionary(data):
        dicData = {}
        keyVal = data.split(',')
        for splited in keyVal:
            keyValSplited = splited.split('=')
            dicData[keyValSplited[0]] = keyValSplited[1]
        return dicData
    
    # Check if data is not negative or 0 (data  = dictionary)
    @staticmethod
    def checkDataValid(data):
        # TODO : Fix the filter paramter
        # Check Temperature
        if 'temp' in data:
            if float(data['temp']) <= 0:
                return False
        # Check Hummidity
        if 'hummidity' in data:
            if float(data['pressure']) <= 0:
                return False
        # Check Pressure
        if 'pressure' in data:
            if float(data['pressure']) <= 0:
                return False
        # If Valid Return True
        return True


# Debug
now = datetime.now()
dataDummy = "abc,{},-5.209925,119.473513,{}".format(str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))
dataDummy2 = "abc,{},{}".format(str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))

# print("Debugging : DataUtils.subscriberPayloadToString")
# print(DataUtils.subscriberPayloadToString("temp", dataDummy2))

# print("Debugging : DataUtils.stringToDictionary")
# print(DataUtils.che(DataUtils.subscriberPayloadToString("temp", dataDummy2)))

print("Debugging : DataUtils.checkDataValid")
print(DataUtils.checkDataValid(DataUtils.stringToDictionary(DataUtils.subscriberPayloadToString("temp", dataDummy))))
