# Copyright (c) 2020 m4nzm333
# Program for file management
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

import os
import datetime


class Datalog:

    # Make directory for data now
    @staticmethod
    def createDirDate(datetime):
        try:
            os.makedirs("./data/subscriber/{}/{}/{}/{}/{}".format(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute))
        except OSError as e:
            pass
    
    # Output the data (string) into file
    @staticmethod
    def writeStringToFile(data):
        now = datetime.datetime.now()
        dirLoc = "./data/subscriber/{}/{}/{}/{}/{}".format(now.year, now.month, now.day, now.hour, now.minute)
        Datalog.createDirDate(now)

        file = open("{}/{}-{}-{} {}:{}:{}.{}.txt".format(dirLoc, now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond), "a")
        file.write(data)
        file.close()
    
    
        

Datalog.writeStringToFile("This is Data")