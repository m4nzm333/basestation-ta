# Copyright (c) 2020 m4nzm333
# Source code for I/O datalog archive save into file
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import datetime
import os
import json

def saveJsonIntoFile(json_string):

    now = datetime.datetime.now()
    lastYear = str(now.year)
    lastMonth = '{:02d}'.format(now.month)
    lastDay = '{:02d}'.format(now.day)
    lastHour = '{:02d}'.format(now.hour)
    lastMinute = '{:02d}'.format(now.minute)

    # The path of arcive file should be /home/pi/data/2020/1/12/21
    dir = "/home/pi/data/{:s}/{:s}/{:s}/{:s}/".format(lastYear, lastMonth, lastDay, lastHour)
    if not os.path.exists(dir):
        os.makedirs(dir)

    # The filename should be 2019-1-12-21-31-15.json
    fileku = open(dir+"{:s}-{:s}-{:s}-{:s}-{:s}.json".format(lastYear, lastMonth, lastDay, lastHour, lastMinute), 'a+')
    fileku.write(json_string)
    fileku.write("\n")
    fileku.close