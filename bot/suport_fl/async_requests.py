import os
from dotenv import load_dotenv
import aiohttp
import asyncio
from suport_fl.setting import *


# Файл для запросов aiohttp
async def _get(**kwargs):
    host = kwargs.get('host')
    path = kwargs.get('path')
    param = kwargs.get('param')
    header = kwargs.get('header')
    address = host + path
    async with aiohttp.ClientSession() as session:
        # Ловим исключения
        try:
            async with session.get(address, headers=header, params=param) as resp:
                return await resp.json()
        except aiohttp.client_exceptions.ClientConnectorError as e:
            return f"Error: {e}"


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


# Функция для тестирования запросов
async def main(host, param):
    req = AioRequests(host, param)
    total = await req.get_request(path='http://127.0.0.1:8000/admin/clients/certificates/add/',)
    # with open('./meteo.json', 'w') as j_file:
    #     json.dump(total, j_file, indent=6, ensure_ascii=True)
    print(total)


if __name__ == '__main__':
    load_dotenv()
    api_key = str(os.getenv("ACCESS_KEY"))
    asyncio.run(main(host='http://127.0.0.1:8000/admin/clients/certificates/add/', param={}))
