import requests
from envparse import Env
import json
import os


def getreq(lat, lon, APIKEY):
    param = {'lang': 'ru',
             'lat': lat,
             'lon': lon,
             'appid': APIKEY,
             'units': 'metric'
             }
    info = requests.get(f'https://api.openweathermap.org/data/2.5/forecast', params=param)
    return json.loads(info.text)


def add_main():
    env = Env()
    APIKEY = env.str("APIKEY")
    city_dict = {'Казань': getreq(lat=55.7890, lon=49.1220, APIKEY=APIKEY),
                 'Инополис': getreq(lat=55.7636, lon=48.7366, APIKEY=APIKEY),
                 'Лаишево': getreq(lat=54.4040, lon=49.5490, APIKEY=APIKEY)}
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'weather.json')
    os.remove(path)
    with open('weather.json', 'w') as file:
        json.dump(city_dict, file)


if __name__ == "__main__":
    add_main()