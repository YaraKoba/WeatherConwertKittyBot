from telebot import types
from functions.mess import amdate
from datetime import date, timedelta


def c_d(numb: int):
    delta = timedelta(days=numb)
    return date.today() + delta


def day_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(amdate(str(c_d(0))))
    btn2 = types.KeyboardButton(amdate(str(c_d(1))))
    btn3 = types.KeyboardButton(amdate(str(c_d(2))))
    btn4 = types.KeyboardButton(amdate(str(c_d(3))))
    btn5 = types.KeyboardButton(amdate(str(c_d(4))))
    btn6 = types.KeyboardButton(f'Все летные дни!')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup