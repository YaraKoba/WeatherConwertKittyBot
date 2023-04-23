import os

from suport_fl.setting import *
from suport_fl.async_requests import AioRequests
from suport_fl.support import create_table
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
    header = ['from', 'to', 'rate']
    row = [[answer["from"], answer["to"], format(answer["rate"], ".3f")],
           [amount, format(float(amount) * answer["rate"], ".2f"), format(answer["rate"], ".3f")]]
    table = create_table(header, row)
    return f'Все готово!\n\n' \
           f'<pre>{table}</pre>'
