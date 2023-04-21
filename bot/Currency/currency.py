import os
import asyncio

from suport_fl.setting import *
from suport_fl.async_requests import AioRequests

from dotenv import load_dotenv


class Currency:
    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.req = AioRequests(host=CUR_API_HOST, param={})

    async def get_cur(self, cur_to, cur_from, amount):
        api_key = str(os.getenv("API_CUR_KEY"))
        result = await self.req.get_request(path=CUR_API_PATH,
                                            header={'apikey': api_key},
                                            new_param={'to': cur_to,
                                                       'from': cur_from,
                                                       'amount': amount})
        return result


def create_cur_text(answer, amount):
    return f'{amount} {answer["from"]} в {answer["to"]} по курсу {answer["rate"]}\n' \
           f'<b>ОТВЕТ: {str(float(amount) * answer["rate"])[:4]} {answer["to"]}</b>'
