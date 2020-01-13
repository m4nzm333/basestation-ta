import json
import time
from datetime import datetime

dummyString = "id=123456;temp=10;timestamp=2019-11-15 06:04:22.123123"

# String dari MQTT ke Objek JSON dan siap di normalisasi ke Database Temp
def receivedStringToJson(stringData):
    splittedArray = stringData.split(';')
    jsonResult = {}
    jsonResult["data"] = {}
    # Bongkar setiap Element -> Output : String KeyValue
    for rawVarVal in splittedArray:
        # Bongkar setiap String KeyValue -> Output : Key dan atau Value
        splittedVarVal = rawVarVal.split(';')
        for keyVal in splittedVarVal:
            splittedAtom = keyVal.split('=')
            if splittedAtom[0] == 'id':
                jsonResult['id_sensor'] = splittedAtom[1]
            elif splittedAtom[0] == 'timestamp':
                jsonResult['sensing_timestamp'] = splittedAtom[1]
            else:
                jsonResult["data"][splittedAtom[0]] = splittedAtom[1]
    # Get now timestamp dan set id data sesuai millis + ms
    jsonResult['id'] = datetime.today().strftime('%s%f')
    jsonResult['basestation_timestamp'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
    jsonResult['status'] = 'temp'

    # print(json.dumps(jsonResult))
    return jsonResult

# Build Json saat data ingin dikirim ke server
def sendingJson(jsonData):
    jsonData['sending_timestamp'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
    jsonData['status'] = 'sending'
    return jsonData

# Build Json saat data telah diterima dan dikonfirmasi oleh Server
def receivedJson(jsonData):
    jsonData['received_timestamp'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
    jsonData['status'] = 'received'
    return jsonData

testSensor = receivedStringToJson(dummyString)
testSending = sendingJson(testSensor)
testReceived = receivedJson(testSending)
print(str(testReceived))
