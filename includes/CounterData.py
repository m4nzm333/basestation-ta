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
                "INSERT INTO counter values ('{}', 0, 0, 0)".format(nowString))
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
                "INSERT INTO counter values ('{}', 0, 0, 0)".format(nowString))
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
                "INSERT INTO counter values ('{}', 0, 0, 0)".format(nowString))
        else:
            cursor.execute(
                "UPDATE counter SET sent = sent+1 WHERE time='{}'".format(nowString))
        conn.commit()
        conn.close()
