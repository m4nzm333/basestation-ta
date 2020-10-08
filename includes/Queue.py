import json
from datetime import datetime
from includes.Config import configMaxNode

def queueLength():
    try:
        config = open('./config/queue.json', 'r')
        config = json.load(config)
        return len(config)
    except:
        return configMaxNode()

def queueIsConnected(id):
    config = open('./config/queue.json', 'r')
    config = json.load(config)
    for sensor in config:
        if sensor['id'] == id:
            return True
    return False

def queueUpdate(id):
    config = open('./config/queue.json', 'r')
    config = json.load(config)
    update = []
    if queueIsConnected(id):
        for sensor in config:
            if sensor['id'] == id:
                sensor['last'] = str(datetime.now())
            update.append(sensor)
    else:
        print(id+" is connected at "+str(datetime.now()))
        for sensor in config:
            update.append(sensor)
        update.append({
            "id": id,
            "last" :  str(datetime.now())
        })
    file = open("./config/queue.json", "w+")
    file.write(json.dumps(update, separators=(",", ":"), sort_keys=True, indent=4))
    file.close()

def queueDelete():
    config = open('./config/queue.json', 'r')
    config = json.load(config)
    update = []
    for sensor in config:
        last = datetime.strptime(sensor['last'], "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.now()
        if (now - last).seconds > 5:
            print(sensor['id'] + " is disconnected at "+str(datetime.now()))
            pass
        else:
            update.append(sensor)
    file = open("./config/queue.json", "w+")
    file.write(json.dumps(update, separators=(",", ":"), sort_keys=True, indent=4))
    file.close()