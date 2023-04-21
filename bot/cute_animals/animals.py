import os
import asyncio

from suport_fl.setting import *
from suport_fl.async_requests import AioRequests

from dotenv import load_dotenv


class Animals:
    def __init__(self):
        api_key = str(os.getenv("ak"))
        self.req = AioRequests(host=KITTY_API_HOST, param={'client_id': api_key})

    async def get_random_animals(self):
        answer = await self.req.get_request(new_param={'query': 'cute animals'}, path=KITTY_API_PATH, header={'Accept-Version': 'v1'})
        return answer['urls']['small']
