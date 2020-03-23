# Copyright (c) 2020 m4nzm333
# Source code for read sensor data from BME280 Module
#   * Temperature
#   * Pressure
#   * Hummidity
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import smbus2
import bme280

class SensorBME280:

    # Address I2C
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    # Get Data from Sensor
    calibration_params = bme280.load_calibration_params(bus, address)

    @staticmethod
    def getTemperature(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature

    @staticmethod
    def getPressure(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.pressure
        
    @staticmethod
    def getHummidity(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.humidity