# Copyright (c) 2020 m4nzm333
# Main Program Python
# Source : https://github.com/m4nzm333/basestation-ta
# Ask a question, please contact:
# e-mail    : irman.mashuri@gmail.com

from RaspiSubscriber import RaspiSubscriber

def main():
    raspiSubscriber = RaspiSubscriber('192.168.1.6', 1883, "Basestation-001")
    print("python main function")

if __name__ == '__main__':
    main()
