# Copyright (c) 2020 m4nzm333
# Source code for read data from Datalog file
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com
# hp/wa     : +6285396397688

import os

# Location of Datalog
rootDir = '/home/pi/data/'

# Year loop
for yearDir in sorted(os.listdir(rootDir)):
    # Flag check
    if yearDir[0:5] == "sent-":
        break
    yearDirLoc = "{:s}{:s}/".format(rootDir, yearDir)

    # Month loop
    for monthDir in sorted(os.listdir(yearDirLoc)):
        # Flag check
        if monthDir[0:5] == "sent-":
            break
        monthDirLoc = "{:s}{:s}/{:s}/".format(rootDir, yearDir, monthDir)

        # Day loop
        for dayDir in sorted(os.listdir(monthDirLoc)):
            # Flag check
            if dayDir[0:5] == "sent-":
                break
            dayDirLoc = "{:s}{:s}/{:s}/{:s}/".format(rootDir, yearDir, monthDir, dayDir)

            # Hour loop
            for hourDir in sorted(os.listdir(dayDirLoc)):
                # Flag check
                if hourDir[0:5] == "sent-":
                    break
                hourDirLoc = "{:s}{:s}/{:s}/{:s}/{:s}/".format(rootDir, yearDir, monthDir, dayDir, hourDir)

                # File Loop
                for fileLoop in sorted(os.listdir(hourDirLoc)):
                    # Flag check
                    if fileLoop[0:5] == "sent-":
                        break
                    print(fileLoop)
                    # TODO : Read file and send data to Server
