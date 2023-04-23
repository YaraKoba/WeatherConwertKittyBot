import os
import asyncio

from suport_fl.setting import OPEN_API_HOST, OPEN_API_PATH
from suport_fl.async_requests import AioRequests

from dotenv import load_dotenv


class WeatherClient:
    def __init__(self, bot):
        load_dotenv()
        api_key = str(os.getenv("API_KEY"))
        self.req = AioRequests(host=OPEN_API_HOST,
                               param={
                                   'lang': 'ru',
                                   'appid': api_key,
                                   'units': 'metric'
                               })
        self.bot = bot
        self.cache_meteo = dict()

    # Получаем прогноз погоды
    async def get_weather(self, city):
        # Если прогноз уже был запрошен на эту горку, то он возьмется из КЭША
        if city in self.cache_meteo:
            print('IN cache')
            result = self.cache_meteo[city]

        # Если нет, то сделать запрос на сервер и записать его в КЭШ
        else:
            print('NOT cache')
            meteo = await self.req.get_request(new_param={'q': city}, path=OPEN_API_PATH)

            # Проверяем успех запроса
            if 'Error' not in meteo and meteo['cod'] == '200':
                self.cache_meteo[city] = meteo

                # Записываем прогноз в КЭШ
                result = self.cache_meteo[city]

                # Запускаем таймер на 1 час, чтобы очистить КЭШ
                loop = asyncio.get_event_loop()
                asyncio.run_coroutine_threadsafe(self.clean_cache(), loop)
            else:
                print(meteo)
                return False
        return result

    # Чистим КЭШ
    async def clean_cache(self):
        await asyncio.sleep(3600)
        self.cache_meteo.clear()
