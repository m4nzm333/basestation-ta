import datetime
import os
import json

def SaveDataIntoFile(object):

    # TODO : convert object to JSON String
    json_string = "{}"

    now = datetime.datetime.now()
    last_year = str(now.year)
    last_month = str(now.month)
    last_day = str(now.day)
    last_hour = str(now.hour)
    dir = "/home/pi/data/"+last_year+"/"+last_month+"/"+last_day+"/"
    if not os.path.exists(dir):
        os.makedirs(dir)

    fileku = open(dir + "/" + last_hour +".json", 'a+')
    fileku.write(json_string)
    fileku.write("\n")
    fileku.close