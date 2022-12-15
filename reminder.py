from envparse import Env
import mess
import button
from database import pull_chat_id
from get_meteo import analytics_main
from row_request import *

env = Env()
TOKEN = env.str("TOKEN")
ADMIN_ID = env.str("ADMIN_ID")
row_req = RowReq(token=TOKEN, base_url='https://api.telegram.org')
bot = MyBot(token=TOKEN, row_req=row_req)

if __name__ == '__main__':
    date_all = button.day_5()
    res = analytics_main(date_all)
    for user_id in pull_chat_id():
        print(user_id)
        if user_id[1] in 'Yes':
            bot.send_message(user_id[0], mess.repost(res), parse_mode='html')
