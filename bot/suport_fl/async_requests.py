import os
import json
from dotenv import load_dotenv
import aiohttp
import asyncio
from suport_fl.setting import *


async def _get(**kwargs):
    host = kwargs.get('host')
    path = kwargs.get('path')
    param = kwargs.get('param')
    header = kwargs.get('header')
    address = host + path
    print(address, param)
    async with aiohttp.ClientSession() as session:
        async with session.get(address, headers=header, params=param) as resp:
            print(resp.text())
            return await resp.json()


class AioRequests:
    def __init__(self, host, param):
        self.host = host
        self.param = param

    async def get_request(self, **kwargs):
        path = kwargs.get('path')
        new_param = kwargs.get('new_param')
        header = kwargs.get('header')
        if new_param:
            for key in new_param:
                self.param[key] = new_param[key]
        return await _get(host=self.host, path=path, param=self.param, header=header)


async def main(host, param):
    req = AioRequests(host, param)
    total = await req.get_request(new_param={'to': 'USD',
                                             'from': 'RUB',
                                             'amount': 10}, path=CUR_API_PATH, header={'apikey': api_key})
    with open('./meteo.json', 'w') as j_file:
        json.dump(total, j_file, indent=6, ensure_ascii=True)
    print(total)


if __name__ == '__main__':
    load_dotenv()
    api_key = str(os.getenv("API_CUR_KEY"))
    asyncio.run(main(host=CUR_API_HOST, param={
        'to': '',
        'from': '',
        'amount': '',
    }))
