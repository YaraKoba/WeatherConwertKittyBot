[![](https://img.shields.io/pypi/pyversions/django-admin-interface.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)

# weather-convert-kitty-bot
Ссылка на бот: https://t.me/test_parakoba_bot

СТЕК: `Python` `aiogram` `aiohhtp`

Бот выполняет следующие функции:

1. Приветствовать пользователя и предлагать ему выбрать определенную функцию бота.
2. Определить текущую погоду в определенном городе, используя публичное API погоды (например, OpenWeatherMap) и выдавать пользователю соответствующую информацию.
3. Конвертировать валюты, используя публичное API курсов валют (например, Exchange Rates API) и предоставлять пользователю результат конвертации.
4. Отправлять случайную картинку с милыми животными
5. Создавать опросы (polls) и отправлять их в групповой чат с определенным вопросом и вариантами ответов.

## Installation

```commandline
git git@github.com:YaraKoba/WeatherConwertKittyBot.git
cd WeatherConwertKittyBot
python -m venv venv
source venv/bin/activate
```

### Install requirements

```commandline
make requirements
```

### Create .env file

```commandline
make env
```
В .env файле заполните следующие поля
```
TOKEN = your telegram token
API_KEY = your key for https://openweathermap.org/api
API_CUR_KEY = your key for https://api.apilayer.com
ACCESS_KEY = your access key for https://api.unsplash.com
```
### Run bot

```commandline
make run_bot
```


