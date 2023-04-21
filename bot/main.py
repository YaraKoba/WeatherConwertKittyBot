#!/usr/bin/env python3
import re
from suport_fl import mess, button, suport
from weather.get_meteo import create_text
from dotenv import load_dotenv
import os

import logging
from weather.weather_main import WeatherClient
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

weather = WeatherClient(bot)


# Форма для прогноза погоды
class FormWeather(StatesGroup):
    city = State()
    date = State()

# Форма для конвектора валют
class FormCurrency(StatesGroup):
    cur = State()
    sum = State()


# Выводим кнопки с выбором функций бота
@dp.message_handler(commands='start')
async def start_help(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    mes = mess.header_mess(message)
    print(message)
    change_btn = button.change_function_btn()
    await message.answer(mes, parse_mode='html', reply_markup=change_btn)


# Сюда приходит callback с выбронной функцией
@dp.callback_query_handler(lambda x: x.data in ['Погода', 'Валюты', 'Котики!', 'Опросы'])
async def process_callback_one_spot(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали {callback_query.data}.")
    # В зависимости от выбранной функции зупускаем диалог
    if callback_query.data == 'Погода':
        await FormWeather.city.set()
        await bot.send_message(callback_query.from_user.id, 'Введите название города')
    elif callback_query.data == 'Валюты':
        await FormCurrency.cur.set()
        await bot.send_message(callback_query.from_user.id, 'Введите название валют через пробел\nнапример RUB USD')


# Эта функция позволяет выйти из диалога командой /cancel
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отмана')


# ПРОГНОЗ проверяем и записываем город
@dp.message_handler(state=FormWeather.city)
async def process_name(message: types.Message, state: FSMContext):
    if not await weather.get_weather(message.text):
        return await message.reply("Город не найден. Попробуйте еще раз или /cancel")

    async with state.proxy() as data:
        data['city'] = message.text

    await FormWeather.next()
    markup = button.day_btn()
    await message.reply("На какую дату сформировать прогноз?\nУкажите дату кнопкой на клавиатуре", reply_markup=markup)


# ПРОГНОЗ проверяем дату
@dp.message_handler(lambda message: not re.search(r"[А-Я][а-я]\s\d{2}\s[а-я]+\b|Сейчас", message.text), state=FormWeather.date)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Дата не верна. Укажите дату кнопкой на клавиатуре или /cancel")


# ПРОГНОЗ записываем дату, отправляем прогноз
@dp.message_handler(state=FormWeather.date)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
        markup = button.change_function_btn()
        meteo = await weather.get_weather(data['city'])
        date_f = [suport.re_amdate(message.text)]
        text = create_text(date_f, meteo)
        await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
    # Заканчиваем диалог
    await state.finish()


@dp.message_handler(state=FormCurrency.cur)
async def process_name(message: types.Message, state: FSMContext):
    if not await weather.get_weather(message.text):
        return await message.reply("Город не найден. Попробуйте еще раз или /cancel")

    async with state.proxy() as data:
        data['cur'] = message.text

    await FormWeather.next()
    markup = button.day_btn()
    await message.reply("На какую дату сформировать прогноз?\nУкажите дату кнопкой на клавиатуре", reply_markup=markup)
#


#
#
# @dp.message_handler(regexp='Погода')
# async def weather(message: types.Message):
#     await Form.city.set()
#     await message.reply("Напиши название города")
#
#
# @dp.message_handler(state=Form.city)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['city'] = message.text
#     await Form.next()
#     await message.reply("Выбери дату")
#
# @dp.message_handler(state=Form.date)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['date'] = message.text
#     await Form.next()
#     await message.reply("Выбери дату")
#
#
#
#
#


# @dip.message_handler(commands='help')
# async def get_help(message: types.Message):
#     print(f'{message.from_user.first_name} - command: {message.text}')
#     mes = mess.help_mess()
#     await message.answer(mes, parse_mode='html')
#
#

#
#
# @dip.message_handler(regexp=r'Все дни!')
# async def all_date_fly(message: types.Message):
#     print(f'{message.from_user.first_name} - command: {message.text}')
#     date_all = button.day_5()
#     weather.get_weather()
#     await message.answer(res, parse_mode='html')
#
#
# @dip.message_handler(regexp=r"[А-Я][а-я]\s\d{2}\s[а-я]+\b")
# async def one_day_fly(message: types.Message):
#     print(f'{message.from_user.first_name} - command: {message.text}')
#     try:
#         date_f = [suport.re_amdate(message.text)]
#         user_inf, spots = await manager.get_user_and_spots(message)
#         res = await manager.create_meteo_message(city=user_inf['city'], chat_id=user_inf['user_id'], lst_days=date_f)
#         await message.answer(res, parse_mode='html')
#     except (IndexError, Exception):
#         await show_days(message)
#
#
# @dip.callback_query_handler(lambda c: c.data)
# async def process_callback_handler(callback_query: types.CallbackQuery):
#     user, spots = await manager.get_user_and_spots(callback_query)
#     spot_dict = None
#     for spot in spots:
#         if callback_query.data == spot['name']:
#             spot_dict = spot
#
#     if spot_dict is not None:
#         res = mess.mess_get_spot(spot_dict)
#         await bot.send_message(user['user_id'], text=res, parse_mode='html')
#     else:
#         city_inf = callback_query.data.split()
#         update_inf = {'city': city_inf[0], 'city_name': city_inf[1]}
#         await manager.update_user(callback_query, update_inf)
#         await bot.send_message(user['user_id'], text=f"Текущее место изменено на: {city_inf[1]}")
#

def ran_server():
    executor.start_polling(dp)


if __name__ == '__main__':
    ran_server()
