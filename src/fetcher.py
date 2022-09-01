#!/usr/bin/env python3

import dateutil.parser
import datetime

import requests


API_KEY = ''  # put your API key here
BASE_URL = 'https://api.airvisual.com/v2/city'
COUNTRY = 'Bangladesh'
STATE = 'Dhaka'
CITY = 'Dhaka'


def get_data():
    """Returns json data if the request is successful, else None
    """
    parameters = {
        'country': COUNTRY,
        'state': STATE,
        'city': CITY,
        'key': API_KEY,
    }

    try:
        res = requests.get(BASE_URL, params=parameters)
        if res.status_code == requests.codes.ok:
            return res.json()
    except Exception as e:
        log = open("/root/AQIndexer/Errors.log", "a")
        log.writelines("{0}\n{1}\n\n".format(datetime.datetime.now(), e))
        log.close()

    return None


def get_datetime(res):
    """Returns the date and time at which we are accessing AQI data
    """
    time = res["data"]["current"]["pollution"]["ts"]
    # Adding 6 hours to convert it to BST
    time = dateutil.parser.parse(time) + datetime.timedelta(hours=6)
    return time.strftime("%Y/%m/%d"), time.strftime("%H:%M")


def get_aqi(res):
    """Returns air quality index (US standard)
    """
    return res["data"]["current"]["pollution"]["aqius"]
