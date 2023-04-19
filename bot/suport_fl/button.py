from aiogram import types
from suport_fl.suport import amdate, get_day


def day_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for day in range(5):
        btn = types.KeyboardButton(amdate(str(get_day(day))))
        markup.add(btn)
    btn = types.KeyboardButton(f'Сейчас')
    markup.add(btn)
    return markup


def change_function_btn():
    name_functions = ['Погода', 'Конвертировать валюты', 'Котики!', 'опросы']
    markup = types.InlineKeyboardMarkup(row_width=1)
    for function in name_functions:
        markup.add(types.InlineKeyboardButton(function, callback_data=function))
    return markup




