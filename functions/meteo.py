import requests
from envparse import Env
import json
import os
from database import get_spot_lat_lon as l_l, get_spot
from functions.button import day_5
from functions.get_meteo import go_fly


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


def add_main(spot_dict: dict, name_file):
    """
    Makes a query from dict 'spot_dict',
    dell old 'name_file',
    and create and write to 'name_file'
    :param spot_dict: dict
    :param name_file: str(name_file.json)
    """
    for city in spot_dict:
        spot_dict[city] = getreq(lat=spot_dict[city][0], lon=spot_dict[city][1])
    try:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'{name_file}')
        os.remove(path)
    except FileNotFoundError:
        print(f'Touch file "{name_file}"')
    with open(f'{name_file}', 'w') as fi:
        json.dump(spot_dict, fi)


def create_new_spot_dict():
    lst_days = day_5()
    go_fly(lst_days)
    # fly_spot = [spot for dct in go_fly(lst_days) for spot in dct['flydict']]
    fly_spot = [spot[0] for spot in get_spot()]
    new_spot_dict = {spot: l_l(spot)[0] for spot in fly_spot}
    return new_spot_dict


if __name__ == "__main__":
    city_dict = {'Казань': [55.7890, 49.1220],
                 'Инополис': [55.7636, 48.7366],
                 'Лаишево': [54.4040, 49.5490]}
    file_weather = 'weather.json'
    file_spot_weather = 'spot_weather.json'
    add_main(city_dict, file_weather)
    add_main(create_new_spot_dict(), file_spot_weather)

