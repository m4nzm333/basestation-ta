# Copyright (c) 2020 m4nzm333
# Program for data counter, error, etc
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import sqlite3
from datetime import datetime
import os
import logging


class CounterData:

    @staticmethod
    def createDir():
        try:
            os.makedirs("./db")
        except:
            pass

    @staticmethod
    def upReceived():
        CounterData.createDir()
        now = datetime.now()
        nowString = datetime.strftime(now, "%Y-%m-%d")

        conn = sqlite3.connect(
            './db/counter.db')
        cursor = conn.cursor()
        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS counter (time text NULL, received BIGINT NULL, blocked BIGINT NULL, sent BIGINT NULL)")
        cursor.execute(
            'SELECT * FROM counter WHERE time="{}"'.format(nowString))
        row = cursor.fetchone()
        if row is None:
            # update
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS counter (time text NULL, received BIGINT NULL, blocked BIGINT NULL, sent BIGINT NULL)")
            cursor.execute(
                "INSERT INTO counter values ('{}', 1, 0, 0)".format(nowString))
        else:
            cursor.execute(
                "UPDATE counter SET received = received+1 WHERE time='{}'".format(nowString))
        conn.commit()
        conn.close()

    @staticmethod
    def upBlocked():
        CounterData.createDir()
        now = datetime.now()
        nowString = datetime.strftime(now, "%Y-%m-%d")

        conn = sqlite3.connect(
            './db/counter.db')
        cursor = conn.cursor()
        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS counter (time text NULL, received BIGINT NULL, blocked BIGINT NULL, sent BIGINT NULL)")
        cursor.execute(
            'SELECT * FROM counter WHERE time="{}"'.format(nowString))
        row = cursor.fetchone()
        if row is None:
            # update
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS counter (time text NULL, received BIGINT NULL, blocked BIGINT NULL, sent BIGINT NULL)")
            cursor.execute(
                "INSERT INTO counter values ('{}', 0, 1, 0)".format(nowString))
        else:
            cursor.execute(
                "UPDATE counter SET blocked = blocked+1 WHERE time='{}'".format(nowString))
        conn.commit()
        conn.close()

    @staticmethod
    def upSent():
        CounterData.createDir()
        now = datetime.now()
        nowString = datetime.strftime(now, "%Y-%m-%d")

        conn = sqlite3.connect(
            './db/counter.db')
        cursor = conn.cursor()
        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS counter (time text NULL, received BIGINT NULL, blocked BIGINT NULL, sent BIGINT NULL)")
        cursor.execute(
            'SELECT * FROM counter WHERE time="{}"'.format(nowString))
        row = cursor.fetchone()
        if row is None:
            # update
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS counter (time text NULL, received BIGINT NULL, blocked BIGINT NULL, sent BIGINT NULL)")
            cursor.execute(
                "INSERT INTO counter values ('{}', 0, 0, 1)".format(nowString))
        else:
            cursor.execute(
                "UPDATE counter SET sent = sent+1 WHERE time='{}'".format(nowString))
        conn.commit()
        conn.close()

    @staticmethod
    def clearCounter(date=None):
        if os.path.exists('./db/counter.db'):
            if date is None:
                os.remove("./db/counter.db")
            else:
                conn = sqlite3.connect(
                    './db/counter.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE counter SET received = 0, blocked = 0, sent = 0 WHERE time='{}'".format(date))
                conn.commit()
                conn.close()

    @staticmethod
    def getCounter(date=None):
        if date is None:
            now = datetime.now()
            date = datetime.strftime(now, "%Y-%m-%d")
        if  os.path.exists('./db/counter.db'):
            conn = sqlite3.connect('./db/counter.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM counter WHERE time='{}'".format(date))
            row = cursor.fetchone()
            if row is None:
                return {
                    'time' : date,
                    'received' : 0,
                    'blocked' : 0,
                    'sent' : 0
                }
            else:
                return {
                    'time' : row[0],
                    'received' : row[1],
                    'blocked' : row[2],
                    'sent' : row[3]
                }
            conn.close()
        else:
            return {
                    'time' : date,
                    'received' : 0,
                    'blocked' : 0,
                    'sent' : 0
                }
