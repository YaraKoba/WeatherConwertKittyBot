from aiogram import types
from datetime import date, timedelta, datetime, timezone
from typing import List
import prettytable as pt


# Функция для создания таблиц prettytable
def create_table(header: list, body: List[List]):
    table_meteo = pt.PrettyTable(header)
    table_meteo.align = 'r'
    for row in body:
        table_meteo.add_row(row)
    return table_meteo


# Возвращает кнопки с функциями бота
def change_function_btn():
    name_functions = ['Погода', 'Валюты', 'Милота!', 'Опросы']
    markup = types.InlineKeyboardMarkup(row_width=1)
    for function in name_functions:
        markup.add(types.InlineKeyboardButton(function, callback_data=function))
    return markup


# Возвращает текуще даты на 5 дней вперед
def day_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for day in range(5):
        # Добавляем кнопки и переводим дату удобный формат
        btn = types.KeyboardButton(amdate(str(get_day(day))))
        markup.add(btn)
    return markup


# Возвращает дату в формате "ПН 01 Января"
def amdate(dat):
    mon_dct = {'01': 'Января', '02': 'февраля', '03': 'марта', '04': 'апреля',
               '05': 'майя', '06': 'июня', '07': 'июля', '08': 'августа',
               '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    week_dict = {1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт', 6: 'Сб', 7: 'Вс'}
    new_dat = str(dat).split('-')
    mon = mon_dct[new_dat[1]]
    day = new_dat[2]
    x = map(int, dat.split('-'))
    week = week_dict[datetime.isoweekday(date(*x))]
    return f'{week} {day} {mon}'


# Меняет формат даты из формата "ПН 01 Января" в "2023-01-01"
def re_amdate(dat: str):
    mon_dct = {'01': 'Января', '02': 'февраля', '03': 'марта', '04': 'апреля',
               '05': 'майя', '06': 'июня', '07': 'июля', '08': 'августа',
               '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    new_dat = str(dat).split(' ')
    mon = ''
    for num in mon_dct:
        if mon_dct[num] == new_dat[2]:
            mon = num
    day = new_dat[1]
    now = datetime.now()
    year = str(now.year)
    return f'{year}-{mon}-{day}'


def get_day(numb: int):
    delta = timedelta(days=numb)
    return date.today() + delta


# Возвращает объект datetime, переводит из формата utc с учетом time_zone
def cheng_format_utc(time_utc, time_zone):
    offset = timedelta(seconds=time_zone)
    dt_object = datetime.fromtimestamp(time_utc, timezone(offset))
    return dt_object
