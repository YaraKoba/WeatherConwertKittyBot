import asyncio

from db.async_requests import RequestToDjango
from suport_fl.set_up import *
from suport_fl.suport import build_user_info
from meteo_analysis import get_meteo
from suport_fl.mess import repost


class ManagerDjango:
    def __init__(self):
        self.req = RequestToDjango(LOCAL_HOST)
        self.cache_meteo = dict()

    async def create_user(self, message):
        mess = build_user_info(message.from_user)
        await self.req.post_new_users(mess)

    async def create_meteo_message(self, message, lst_days: list):
        user_city_id = await self.req.get_user_by_id(str(message.from_user.id))
        spots = await self.req.get_spots_by_city_id({'city_id': str(user_city_id['city'])})
        spot_name = [s['name'] for s in spots]
        result = await asyncio.gather(*(self.req.get_meteo((sp['lat'], sp['lon'])) for sp in spots))
        result_spots_dict = {t: r for (t, r) in zip(spot_name, result)}
        meteo_res = get_meteo.analytics_main(lst_days, result_spots_dict, spots)
        return repost(meteo_res, spots, message.text)
