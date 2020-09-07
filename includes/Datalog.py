# Copyright (c) 2020 m4nzm333
# Program for file management
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import os
from datetime import datetime

def logDir():
    sekarang = datetime.now()
    directory = 'log/{}'.format(sekarang.year)
    if not os.path.exists(directory):
        os.makedirs(directory)

def logWrite(topic, data):
    now = datetime.now()
    sekarang = datetime.strftime(now, "%Y-%m-%d")
    logDir()
    document = 'log/{}/{}.csv'.format(now.year, sekarang)
    file = open(document, "a")
    file.write("{},{}\n".format(topic, data))
    file.close
