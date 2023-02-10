#!/usr/bin/env python3


from suport_fl import button, mess, suport
from dotenv import load_dotenv
import os
# from meteo_analysis.get_meteo import analytics_main


import logging
from aiogram import Bot, Dispatcher, types, executor
from db.manager import ManagerDjango

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dip = Dispatcher(bot=bot)
manager = ManagerDjango()


@dip.message_handler(commands=['start', 'help'])
async def start_help(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    mes = mess.header_mess(message)
    print(message.from_user)
    await manager.create_user(message)
    await message.answer(mes, parse_mode='html')
    await show_days(message)


@dip.message_handler(commands=['days'])
async def show_days(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    markup = button.day_btn()
    await message.answer("Даты обновлены", parse_mode='html', reply_markup=markup)


@dip.message_handler(regexp=r'Все летные дни!')
async def all_date_fly(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    date_all = button.day_5()
    res = await manager.create_meteo_message(message, date_all)
    await message.answer(res, parse_mode='html')


@dip.message_handler(regexp=r"[А-Я][а-я]\s\d{2}\s[а-я]+\b")
async def one_day_fly(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    try:
        date_f = [suport.re_amdate(message.text)]
        res = await manager.create_meteo_message(message, date_f)
        await message.answer(res, parse_mode='html')
    except IndexError:
        await show_days(message)


@dip.message_handler(commands=['go', 'stop'])
async def go_start_reminder(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    if message.text in '/go':
        update_inf = {'get_remainder': True}
        await manager.update_user(message, update_inf)
        await message.answer('Теперь вы будете получать уведомления')
    else:
        update_inf = {'get_remainder': False}
        await manager.update_user(message, update_inf)
        await message.answer('Теперь вы НЕ будете получать уведомления')


@dip.message_handler(commands=['get_spot'])
async def get_spot(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    spots, user = await manager.get_user_and_spots(message)
    markup = button.spots_btn(spots)
    await message.answer(f'Все добавленные горки города {user["city_name"]}', reply_markup=markup)


#
#
# def show_spot(message):
#     if str(message.text).lower() == 'все':
#         bot.send_message(message.chat.id, mess.mess_get_all_spot(db.get_spot()), parse_mode='html')
#     else:
#         res = mess.mess_get_spot(db.get_spot(str(message.text)))
#         bot.send_message(message.chat.id, res, parse_mode='html')


def ran_server():
    executor.start_polling(dip)


if __name__ == '__main__':
    ran_server()
