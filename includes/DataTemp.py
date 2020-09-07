# Copyright (c) 2020 m4nzm333
# Program for file management
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import os
from datetime import datetime
import psutil
import time


def dirTemp():
    sekarang = datetime.now()
    directory = 'temp/{}'.format(sekarang.year)
    if not os.path.exists(directory):
        os.makedirs(directory)


def tempWrite(topic, data):
    now = datetime.now()
    sekarang = datetime.strftime(now, "%Y-%m-%d %H-%M-%S")
    dirTemp()
    document = 'temp/{}/{}.csv'.format(now.year, sekarang)
    file = open(document, "a")
    file.write("{},{}\n".format(topic, data))
    file.close


def isFileUsed(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass
    return False

def getOldestData():
    year = os.listdir('temp/')
    if len(year) == 0:
        return []
    year.sort()
    doc = os.listdir('temp/'+year[0])
    if len(doc) == 0:
        return []
    doc.sort()
    document = 'temp/{}/{}'.format(year[0], doc[0])
    if isFileUsed(document):
        return []
    else:
        file = open(document, 'r')
        data = file.read().splitlines()
    return data

def delOldestData():
    year = os.listdir('temp/')
    if len(year) == 0:
        return
    year.sort()
    doc = os.listdir('temp/'+year[0])
    if len(doc) == 0:
        return
    doc.sort()
    document = 'temp/{}/{}'.format(year[0], doc[0])
    if os.path.isfile(document):
        os.unlink(document)
    doc = os.listdir('temp/'+year[0])
    if len(doc) == 0:
        os.rmdir('temp/'+year[0])