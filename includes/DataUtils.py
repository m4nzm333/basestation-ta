# Copyright (c) 2020 m4nzm333
# Source code for data conversion
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

# Debug
import random
from datetime import datetime
from math import isnan
from includes.Config import configCalibration

def checkValid(sensor, data):
    # sensorTime, sendTime, value, lat, lon, id
    data = data.split(',')
    # If base data rusak
    if len(data) != 4:
        return False
    if data[0] == '2000-00-00 08:00:00.484000':
        return False
    # Conver to Float
    try:
        value = float(data[1])
    except:
        return False
    if value is None or isnan(value):
        return False
    # Check Param Value
    if sensor == 'temperature' and value <= 0:
        return False
    if sensor == 'humidity' and value <= 0:
        return False
    if sensor == 'pressure' and value <= 0:
        return False
    if sensor == 'co2' and value <= 0:
        return False
    if sensor == 'co' and value <= 0:
        return False
    if sensor == 'pm10' and value < 0:
        return False
    return True

def calibrateValue(id, param, value):
    calibrated = round(float(value) + configCalibration(id, param), 2)
    print("| Calibrated | {}, {} , {} => {}".format(id, param, value, calibrated))
    return calibrated
