import json


def getLat():
    try:
        with open('./config/location.json') as json_file:
            data = json.load(json_file)
            return data['lat'] if data['lat'] != 'None' else ''
    except:
        return ''


def getLong():
    try:
        with open('./config/location.json') as json_file:
            data = json.load(json_file)
            return data['long'] if data['long'] != 'None' else ''
    except:
        return ''
