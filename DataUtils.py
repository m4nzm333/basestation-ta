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
        dataRaw = "id={},{}={},".format(delimiter[0], topic, delimiter[1])
        # Check if 3rd data is timestamp
        try:
            datetime.strptime(delimiter[2], "%Y-%m-%d %H:%M:%S.%f")
            return "id={},{}={},timestamp={}".format(delimiter[0], topic, delimiter[1], delimiter[2])
        except:
            return "id={},{}={},long={},lat={},timestamo={}".format(delimiter[0], topic, delimiter[1], delimiter[2], delimiter[3], delimiter[4])
    
# Debug
# now = datetime.now()
# print("Debugging : DataUtils.subscriberPayloadToString")
# dataDummy = "abc,{},-5.209925,119.473513,{}".format(str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))
# dataDummy2 = "abc,{},{}".format(str(random.uniform(28.0, 33.5))[:5], now.strftime("%Y-%m-%d %H:%M:%S.%f"))
# print(DataUtils.subscriberPayloadToString("temp", dataDummy2))
