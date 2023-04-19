import os
import json
from dotenv import load_dotenv
import aiohttp
import asyncio
from suport_fl.setting import OPEN_API_HOST, OPEN_API_PATH, OPEN_API_PATH_RIGHT_NOW


async def _get(host, path, param=None):
    address = host + path
    async with aiohttp.ClientSession() as session:
        async with session.get(address, params=param) as resp:
            return await resp.json()



class AioRequests:
    def __init__(self, host, param):
        self.host = host
        self.param = param

    async def get_request(self, new_param: dict, path):
        for key in new_param:
            self.param[key] = new_param[key]
        return await _get(self.host, path, param=self.param)


async def main(host, param):
    req = AioRequests(host, OPEN_API_PATH, param)
    total = await req.get_request({'q': 'Kazan'})
    # with open('./meteo.json', 'w') as j_file:
    #     json.dump(total, j_file, indent=6, ensure_ascii=True)
    print()


if __name__ == '__main__':
    load_dotenv()
    h = OPEN_API_HOST
    api = str(os.getenv("API_KEY"))
    print(api)
    p = {'lang': 'ru',
         'q': 'Казань',
         'appid': api,
         'units': 'metric'
         }
    asyncio.run(main(h, p))
