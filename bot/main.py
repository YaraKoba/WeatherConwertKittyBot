#!/usr/bin/env python3
import re
import os
import logging
from dotenv import load_dotenv

from suport_fl import mess, support
from weather.get_meteo import create_text
from Currency.currency import Currency, create_cur_text
from weather.weather_main import WeatherClient
from cute_animals.animals import Animals

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
currency = Currency(bot)
kitty = Animals()


# Форма для прогноза погоды
class FormWeather(StatesGroup):
    city = State()
    date = State()


# Форма для конвектора валют
class FormCurrency(StatesGroup):
    cur = State()
    sum = State()


# Форма для polls
class FormPolls(StatesGroup):
    question = State()
    options = State()
    chat_id = State()


# Выводим кнопки с выбором функций бота
@dp.message_handler(commands='start')
async def start(message: types.Message):
    print(f'{message.from_user.first_name} - command: {message.text}')
    mes = mess.header_mess(message)
    print(message)
    change_btn = support.change_function_btn()
    await message.answer(mes, parse_mode='html', reply_markup=change_btn)


# Сюда приходит callback с выбранной функцией
@dp.callback_query_handler(lambda x: x.data in ['Погода', 'Валюты', 'Милота!', 'Опросы'])
async def change_function(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали {callback_query.data}")
    # В зависимости от выбранной функции запускаем диалог
    if callback_query.data == 'Погода':
        await FormWeather.city.set()
        await bot.send_message(callback_query.from_user.id, 'Введите название города')
    elif callback_query.data == 'Валюты':
        await FormCurrency.cur.set()
        await bot.send_message(callback_query.from_user.id, 'Введите название валют через пробел\nнапример RUB USD')
    elif callback_query.data == 'Милота!':
        await send_random_animal_image(callback_query.from_user.id)
    elif callback_query.data == 'Опросы':
        await FormPolls.question.set()
        await bot.send_message(callback_query.from_user.id, mess.polls_mess())


# Эта функция позволяет выйти из диалога командой /cancel
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    markup = support.change_function_btn()
    await message.reply('Отмена. Теперь вы можете снова выбрать опцию', reply_markup=markup)


# ПРОГНОЗ проверяем и записываем город
@dp.message_handler(state=FormWeather.city)
async def process_city(message: types.Message, state: FSMContext):
    # Если запрос на сервер был не успешным, просим повторить попытку
    if not await weather.get_weather(message.text):
        return await message.reply("Город не найден. Попробуйте еще раз или /cancel")

    async with state.proxy() as data:
        data['city'] = message.text

    await FormWeather.next()
    markup = support.day_btn()
    await message.reply("На какую дату сформировать прогноз?\nУкажите дату кнопкой на клавиатуре", reply_markup=markup)


# ПРОГНОЗ проверяем дату
@dp.message_handler(lambda message: not re.search(r"[А-Я][а-я]\s\d{2}\s[а-я]+\b", message.text),
                    state=FormWeather.date)
async def process_date_invalid(message: types.Message):
    return await message.reply("Дата не верна. Укажите дату кнопкой на клавиатуре или /cancel")


# ПРОГНОЗ записываем дату, отправляем прогноз
@dp.message_handler(state=FormWeather.date)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
        meteo = await weather.get_weather(data['city'])
        date_f = [support.re_amdate(message.text)]
        text = create_text(date_f, meteo)
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, 'Ваш прогноз готов!', reply_markup=markup, parse_mode='html')
        markup = support.change_function_btn()
        await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
    # Заканчиваем диалог
    await state.finish()


# ВАЛЮТЫ принимаем обозначения валют и проверяем на валидность
@dp.message_handler(state=FormCurrency.cur)
async def process_value(message: types.Message, state: FSMContext):
    user_text = message.text.split()
    # Проверяем, что введено всего 2 значения
    if len(user_text) == 2:
        cur_from = user_text[0].upper()
        cur_to = user_text[1].upper()
    else:
        await bot.send_message(message.from_user.id,
                               'Нужно указать 2 параметра из какой и в какую валюту хотите менять')
        return
    # Делаем запрос на сервер, чтобы проверить введенные данные
    await bot.send_message(message.from_user.id, 'Делаем запрос на сервер...')
    answer = await currency.get_cur(cur_to, cur_from, 100)
    if 'error' in answer:
        return await message.reply("Обозначения валют введены не верно или ошибка на сервере. "
                                   "Попробуйте еще раз или /cancel")

    # В случае успеха записываем данные в форму
    async with state.proxy() as data:
        data['cur'] = {'to': cur_to, 'from': cur_from, 'rate': answer["info"]["rate"]}

    await FormCurrency.next()
    await message.reply(f"Введите сумму {cur_from} чтобы перевести в {cur_to}")


# ВАЛЮТЫ принимаем сумму конвертации и проверяем на валидность, выводим ответ
@dp.message_handler(state=FormCurrency.sum)
async def process_sum(message: types.Message, state: FSMContext):
    # Проверяем введенную сумму, что это цифра и, что она не более 10 знаков.
    if not message.text.isdigit() or len(message.text) > 10:
        await bot.send_message(message.chat.id, 'Вводить только цифры длиной не более 10 знаков')
        return
    async with state.proxy() as data:
        amount = data['sum'] = message.text
        # Формируем сообщение с результатом для отправки
        text = create_cur_text(data['cur'], amount)
        markup = support.change_function_btn()
        await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
    # Заканчиваем диалог
    await state.finish()


# ОПРОСЫ принимаем вопрос для опроса
@dp.message_handler(state=FormPolls.question)
async def process_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await FormPolls.next()
    await message.reply("Напишите опции для ответа через запятую.\n"
                        "например: 'Отличное, Хорошее, Плохое'\nДля отмены введите /cancel")


# ОПРОСЫ принимаем опции и проверяем их количество
@dp.message_handler(state=FormPolls.options)
async def check_options(message: types.Message, state: FSMContext):
    options = message.text.split(sep=',')

    # Проверяем количество опций, не менее 2х
    if len(options) < 2:
        await bot.send_message(message.from_user.id, 'Нужно написать минимум 2 опции через запитую')
        return
    async with state.proxy() as data:
        data['options'] = options

        # Предварительный просмотр опроса
        await bot.send_poll(message.from_user.id, data["question"], data["options"])
        await FormPolls.next()
        await bot.send_message(message.from_user.id, "Введите id группы куда отправить опрос\n"
                                                     "Для отмены введите /cancel")


# ОПРОСЫ принимаем id группы и проверяем на валидность, отправляем опрос
@dp.message_handler(state=FormPolls.chat_id)
async def process_chat_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # С помощью регулярных выражений находим из сообщения пользователя id чат группы
        chat_id = re.findall(r'-?\d+', message.text)
        data['chat_id'] = chat_id[0]

        # Проверяем, существует ли чат
        try:
            markup = support.change_function_btn()
            await bot.send_poll(data["chat_id"], data["question"], data["options"])
            await bot.send_message(message.from_user.id, f"Опрос успешно доставлен на id: {data['chat_id']}",
                                   reply_markup=markup)
        except Exception as err:
            print(err)
            if str(err) == 'Chat not found':
                await message.reply("Чат не найден, повторите попытку или /cancel")
                return

        await state.finish()


# Узнаем id чата
@dp.message_handler(commands=['get_chat_id'])
async def get_chat_id(message: types.Message):
    await message.reply(f"id чата: {message.chat.id}")


# Отправляем рандомную фото милого животного
async def send_random_animal_image(chat_id: int):
    image_url = await kitty.get_random_animals()
    markup = support.change_function_btn()
    if image_url:
        await bot.send_photo(chat_id, image_url, reply_markup=markup)
    else:
        await bot.send_message(chat_id, 'Что-то пошло не так, повторите попытку позже')


def ran_server():
    executor.start_polling(dp)


if __name__ == '__main__':
    ran_server()
