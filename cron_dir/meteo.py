#!/usr/bin/env python3

import requests
from envparse import Env
import json
from db.database import DataBase


def getreq(lat, lon):
    env = Env()
    APIKEY = env.str("APIKEY")
    param = {'lang': 'ru',
             'lat': lat,
             'lon': lon,
             'appid': APIKEY,
             'units': 'metric'
             }
    info = requests.get(f'https://api.openweathermap.org/data/2.5/forecast', params=param)
    return json.loads(info.text)


def add_main(spot_dict: dict, name_file='spot_weather.json'):
    """
    Makes a query from dict 'spot_dict',
    dell old 'name_file',
    and create and write to 'name_file'
    :param spot_dict: dict
    :param name_file: str(name_file.json)
    """
    for city in spot_dict:
        spot_dict[city] = getreq(lat=spot_dict[city][0], lon=spot_dict[city][1])
    with open(f'/Users/yarakoba/PycharmProjects/para_kzn_bot/db/{name_file}', 'w') as fi:
        json.dump(spot_dict, fi)


if __name__ == "__main__":
    print("Прогноз обновлен")
    db = DataBase('/Users/yarakoba/PycharmProjects/para_kzn_bot/db/bot_db.db')
    sp_dict = db.create_new_spot_dict()
    add_main(sp_dict)

