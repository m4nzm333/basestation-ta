import json


def configServerHostname():
    config = open('./config/config.json', 'r')
    config = json.load(config)
    return config['serverHostname']


def configServerDelay():
    config = open('./config/config.json', 'r')
    config = json.load(config)
    return float(config['serverDelay'])


def configSensor():
    config = open('./config/config.json', 'r')
    config = json.load(config)
    return bool(config['sensorOn'])
