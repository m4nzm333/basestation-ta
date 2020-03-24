# Copyright (c) 2020 m4nzm333
# Source code for read sensor data from BME280 Module
#   * Temperature : Celcius
#   * Pressure : hPa (HectoPascal or 100 Pascal)
#   * Hummidity : %
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import smbus2
import bme280
import logging

class SensorBME280:

    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)

    def __init__(self):
        logging.basicConfig(filename='./log/bme280.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
            
    def getTemperature(self):
        try:
            data = bme280.sample(self.bus, self.address, self.calibration_params)
            return data.temperature
        except:
            logging.exception("BME280: Get temperature failed")
            return 0
            
    def getPressure(self):
        try:
            data = bme280.sample(self.bus, self.address, self.calibration_params)
            return data.pressure
        except:
            logging.exception("BME280: Get pressure failed")
            return 0
            
    def getHummidity(self):
        try:
            data = bme280.sample(self.bus, self.address, self.calibration_params)
            logging.exception("BME280: Get hummidity failed")
            return data.humidity
        except:
            return 0
