import aiohttp
import asyncio
from suport_fl.set_up import *


async def _get(host, path, param=None):
    address = host + path
    async with aiohttp.ClientSession() as session:
        async with session.get(address, params=param) as resp:
            return await resp.json()


async def _post(host, path, data=None):
    address = host + path
    async with aiohttp.ClientSession() as session:
        async with session.post(address, data=data) as resp:
            print(resp.status)
            return await resp.json()


class RequestToDjango:
    def __init__(self, host):
        self.host = host

    async def get_all_users(self):
        return await _get(self.host, USER_PATH)

    async def get_user_by_id(self, user_id: str):
        return await _get(self.host, USER_PATH + user_id)

    async def get_spots_by_city_id(self, city_id):
        return await _get(self.host, SPOTS_PATH, param=city_id)

    async def post_new_users(self, inf_usr):
        return await _post(self.host, USER_PATH, data=inf_usr)

    async def get_meteo(self, latlon):
        latlon = tuple(latlon)
        APIKEY = '11c0d3dc6093f7442898ee49d2430d20'
        param = {'lang': 'ru',
                 'lat': latlon[0],
                 'lon': latlon[1],
                 'appid': APIKEY,
                 'units': 'metric'
                 }
        return await _get(OPEN_API_HOST, OPEN_API_PATH, param=param)


async def main(ht, mess, l):
    req = RequestToDjango(ht)
    # print(await req.get_all_users())
    # print(await req.get_user_by_id('356760688'))
    # print(await req.get_spots_by_city_id({'city_id': '1'}))
    # print(await req.post_new_users(mess))
    tasks = [req.get_meteo(i) for i in l]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    ll = [['55.3126', '49.145']] * 20
    mes = {'user_id': 1111, 'city_name': 'Kazan', 'username': 'test', 'first_name': 'test', 'last_name': 'test',
           'language_code': 'ru', 'is_blocked_bot': False, 'is_banned': False, 'is_admin': False, 'is_moderator': False,
           'get_remainder': True, 'city': 1}
    htt = 'http://localhost:63994'
    asyncio.run(main(htt, mes, ll))
