#!/usr/bin/env python3

from dotenv import load_dotenv
from suport_fl import button
import os


import logging
from aiogram import Bot
from db.manager import ManagerDjango

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
manager = ManagerDjango(bot)

if __name__ == '__main__':
    date_all = button.day_5()
    res = manager.create_meteo_message()
    for user in pull_chat_id():
        print(user)
        if user[2] in 'Yes':
            bot.send_message(user[1], mess.repost(res), parse_mode='html')
