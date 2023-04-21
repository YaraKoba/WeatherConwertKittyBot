import os
import asyncio

from suport_fl.setting import *
from suport_fl.async_requests import AioRequests

from dotenv import load_dotenv


class WeatherClient:
    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        api_key = str(os.getenv("API_CUR_KEY"))
        self.req = AioRequests(host=CUR_API_HOST, param={
            'to': '',
            'from': '',
            'amount': '',
            'apikey': api_key,
        })
        self.cache_meteo = dict()

    async def get_cur(self, cur_to, cur_from, amount):

        print('NOT cache')
        result = await self.req.get_request(path=OPEN_API_PATH, new_param={'to': cur_to,
                                                                           'from': cur_from,
                                                                           'amount': amount})
        print(result['cod'])
        return result if result['cod'] == '200' else False
