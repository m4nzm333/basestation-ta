# Copyright (c) 2020 m4nzm333
# Program for data gathering to sql
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import sqlite3
from datetime import datetime
import os
import logging


class SqlMonitor:

    # Make directory for data now
    @staticmethod
    def createDir():
        try:
            os.makedirs("./db/data")
        except:
            pass

    # Write to SQL
    @staticmethod
    def sqlWrite(topic, data, nowString):
        # Login
        logging.basicConfig(filename='./log/sqlite.log',
                            format='%(asctime)s %(message)s', level=logging.DEBUG)
        try:
            SqlMonitor.createDir()
            delimiter = data.split(',')
            sensorDate = datetime.strptime(
                delimiter[0], "%Y-%m-%d %H:%M:%S.%f")

            conn = sqlite3.connect(
                './db/data/{}-{}-{}.db'.format(sensorDate.year, sensorDate.month, sensorDate.day))
            c = conn.cursor()
            # Create table
            c.execute("CREATE TABLE IF NOT EXISTS '%s' (sensorTime text NULL, sensorSendTime TEXT NULL, receivedTime text NULL, sendTime text NULL, confirmationTime, id, value, lat NULL, long NULL)" % topic)
            item = (delimiter[0], delimiter[1], nowString, None, None,
                    delimiter[5], delimiter[2], delimiter[3], delimiter[4])
            c.execute("INSERT INTO '%s' values (?, ?, ?, ?, ?, ?, ?, ?, ?)" %
                      topic, item)
            conn.commit()
            conn.close()
        except:
            logging.exception("Error at writing db sql")

    @staticmethod
    def sqlUpdate(idSensor, sensorDateStr, topic, sendTime):
        sensorDate = datetime.strptime(
            sensorDateStr, "%Y-%m-%d %H:%M:%S.%f")
        conn = sqlite3.connect(
            './db/{}-{}-{}.db'.format(sensorDate.year, sensorDate.month, sensorDate.day))
        c = conn.cursor()
        # print()
        query = 'UPDATE {} SET sendTime = "{}" WHERE id = "{}" AND sensorTime = "{}"'.format(topic, sendTime, idSensor, sensorDateStr)
        c.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def getQuery(stringQuery):
        conn = sqlite3.connect('./db/2020-8.db')
        c = conn.cursor()
        data = []
        for row in c.execute(stringQuery):
            time, value = row
            data.append({'time': time, 'value': value})
        conn.close()
        return data

# SqlMonitor.createDir()
# topic = 'co2'
# conn = sqlite3.connect('./db/abu.db')
# c = conn.cursor()
# # Create table
# c.execute("CREATE TABLE IF NOT EXISTS '%s' (date text NULL, trans text, symbol text, qty real, price real)" % topic)
# c.execute("INSERT INTO '%s' VALUES ('2006-01-05','BUY','RHAT',100,35.14)" % topic)
# conn.commit()
# conn.close()
