import json

dummyString = "id=123456;temp=10;timestamp=2019-11-15-06:04:22.123123"

# String dari MQTT ke Objek JSON dan siap di normalisasi ke Database Temp
def stringToJson(stringData):
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
                jsonResult[splittedAtom[0]] = splittedAtom[1]
            elif splittedAtom[0] == 'timestamp':
                jsonResult[splittedAtom[0]] = splittedAtom[1]
            else:
                jsonResult["data"][splittedAtom[0]] = splittedAtom[1]


    print(json.dumps(jsonResult))
stringToJson(dummyString)