# Copyright (c) 2020 m4nzm333
# Program for data gathering to sql
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import sqlite3
from datetime import datetime
import os

def createDir():
    directory = 'db/data'
    if not os.path.exists(directory):
        os.makedirs(directory)

def sqlWrite(topic, data, recTime):
    createDir()
    sensorTime, sensorSend, value, lat, lon, idSensor= data.split(',')
    now = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect('./db/data/{}.db'.format(now))
    c = conn.cursor()
    # Create table
    c.execute("CREATE TABLE IF NOT EXISTS data (sensorTime text NULL, sensorSend TEXT NULL, receivedTime text NULL, sendTime text NULL, topic text, id text, value text, lat NULL, long NULL)")
    query = "INSERT INTO data values ('{}', '{}', '{}', '', '{}', '{}', '{}', '{}', '{}')".format(sensorTime, sensorSend, recTime, topic, idSensor, value, lat, lon)
    c.execute(query)
    conn.commit()
    conn.close()
    
def sqlUpdate(idSensor, sensorDateStr, topic, sendTime):
    now = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(
        './db/data/{}.db'.format(now))
    c = conn.cursor()

    query = 'UPDATE data SET sendTime = "{}" WHERE id = "{}" AND sensorTime = "{}" AND topic = "{}"'.format(
        sendTime, idSensor, sensorDateStr, topic)
    c.execute(query)
    conn.commit()
    conn.close()
