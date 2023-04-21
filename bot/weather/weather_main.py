import os
import asyncio

from suport_fl.setting import OPEN_API_HOST, OPEN_API_PATH, OPEN_API_PATH_RIGHT_NOW
from suport_fl.async_requests import AioRequests

from dotenv import load_dotenv


class WeatherClient:
    def __init__(self, bot):
        load_dotenv()
        api_key = str(os.getenv("API_KEY"))
        self.req = AioRequests(host=OPEN_API_HOST,
                               param={
                                   'lang': 'ru',
                                   'q': 'Казань',
                                   'appid': api_key,
                                   'units': 'metric'
                               })
        self.bot = bot
        self.cache_meteo = dict()

    async def get_weather(self, city):
        if city in self.cache_meteo:
            print('IN cache')
            result = self.cache_meteo[city]
        else:
            print('NOT cache')
            meteo = await self.req.get_request(new_param={'q': city}, path=OPEN_API_PATH)
            print(meteo['cod'])
            if meteo['cod'] == '200':
                self.cache_meteo[city] = meteo
                result = self.cache_meteo[city]
                loop = asyncio.get_event_loop()
                asyncio.run_coroutine_threadsafe(self.clean_cache(), loop)
            else:
                return False
        return result

    async def get_weather_right_now(self, city):
        meteo = await self.req.get_request(new_param={'q': city}, path=OPEN_API_PATH_RIGHT_NOW)
        if meteo['cod'] == '200':
            return meteo
        else:
            return False

    async def clean_cache(self):
        await asyncio.sleep(3600)
        self.cache_meteo.clear()
