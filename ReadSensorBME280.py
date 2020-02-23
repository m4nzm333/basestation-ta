# Copyright (c) 2020 m4nzm333
# Source code for read sensor data from BME280 Module
#   * Temperature
#   * Pressure
#   * Hummidity
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import smbus2
import bme280

# Address I2C
port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

def getTemperature():
    data = bme280.sample(bus, address, calibration_params)
    return data.temperature

def getPressure():
    data = bme280.sample(bus, address, calibration_params)
    return data.pressure

def getHummidity():
    data = bme280.sample(bus, address, calibration_params)
    return data.humidity