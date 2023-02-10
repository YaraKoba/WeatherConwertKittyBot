import asyncio

from db.async_requests import RequestToDjango
from suport_fl.set_up import *
from suport_fl.suport import build_user_info
from meteo_analysis import get_meteo
from suport_fl.mess import repost


class ManagerDjango:
    def __init__(self):
        self.req = RequestToDjango(LOCAL_HOST, OPEN_API_HOST)
        self.cache_meteo = dict()

    async def create_user(self, message):
        mess = build_user_info(message.from_user)
        await self.req.post_new_users(mess)

    async def update_user(self, message, update_inf):
        mess = build_user_info(message.from_user, update_inf)
        await self.req.put_update_users(mess)

    async def get_user_and_spots(self, message):
        user_info = await self.req.get_user_by_id(str(message.from_user.id))

        if len(user_info) < 2:
            await self.create_user(message)
            user_info = await self.req.get_user_by_id(str(message.from_user.id))

        spots = await self.req.get_spots_by_city_id({'city_id': str(user_info['city'])})
        return user_info, spots

    async def create_meteo_message(self, message, lst_days: list):
        user_info = await self.req.get_user_by_id(str(message.from_user.id))

        if len(user_info) < 2:
            await self.create_user(message)
            user_info = await self.req.get_user_by_id(str(message.from_user.id))

        spots = await self.req.get_spots_by_city_id({'city_id': str(user_info['city'])})

        if user_info['city'] in self.cache_meteo:
            print('IN cache')
            result = self.cache_meteo[user_info['city']]
        else:
            print('NOT cache')
            self.cache_meteo[user_info['city']] = await asyncio.gather(*(self.req.get_meteo((sp['lat'], sp['lon']))
                                                                         for sp in spots))
            result = self.cache_meteo[user_info['city']]
            loop = asyncio.get_event_loop()
            asyncio.run_coroutine_threadsafe(self.clean_cache(), loop)

        spot_name = [s['name'] for s in spots]
        result_spots_dict = {t: r for (t, r) in zip(spot_name, result)}
        meteo_res = get_meteo.analytics_main(lst_days, result_spots_dict, spots)
        return repost(meteo_res, spots, message.text)

    async def clean_cache(self):
        await asyncio.sleep(3600)
        self.cache_meteo.clear()

