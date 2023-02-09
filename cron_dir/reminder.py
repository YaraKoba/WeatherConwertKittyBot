#!/usr/bin/env python3

from envparse import Env
from suport_fl import button, mess
from db.database import pull_chat_id
from meteo_analysis.get_meteo import analytics_main
from suport_fl.row_request import *

env = Env()
TOKEN = env.str("TOKEN")
row_req = RowReq(token=TOKEN, base_url='https://api.telegram.org')
bot = MyBot(token=TOKEN, row_req=row_req)

if __name__ == '__main__':
    date_all = button.day_5()
    res = analytics_main(date_all)
    for user in pull_chat_id():
        print(user)
        if user[2] in 'Yes':
            bot.send_message(user[1], mess.repost(res), parse_mode='html')
