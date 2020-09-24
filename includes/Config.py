import json


def configServer():
    config = open('./config/config.json', 'r')
    config = json.load(config)
    return bool(config['serverOn'])

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

def configTopic():
    config = open('./config/node.json', 'r')
    config = json.load(config)
    topic = []
    for node in config:
        for param in node['parameter']:
            topic.append((node['id']+'/'+param['name'], 0))
    return topic

def configMaxNode():
    config = open('./config/config.json', 'r')
    config = json.load(config)
    return config['maxNode']

def configCalibration(idNode, parameter):
    config = open('./config/node.json', 'r')
    config = json.load(config)
    for node in config:
        if node['id'] == idNode:
            for param in node['parameter']:
                if param['name'] == parameter:
                    
                    return param['calibration']
            break
    return 0
