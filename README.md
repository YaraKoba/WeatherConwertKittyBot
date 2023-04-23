[![](https://img.shields.io/pypi/pyversions/django-admin-interface.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)

# weather-convert-kitty-bot
Ссылка на бот: https://t.me/test_parakoba_bot

СТЕК: `Python` `aiogram` `aiohhtp`

Бот выполняет следующие функции:

1. Приветствует пользователя и предлагает ему выбрать определенную функцию бота.
2. Определяет погоду в определенном городе по дате, используя OpenWeatherMap и выводит пользователю информацию в таблице.
3. Конвертирует валюты, используя публичное API https://api.apilayer.com и предоставляет пользователю результат конвертации.
4. Отправляет случайную картинку с милыми животными, используя https://api.unsplash.com
5. Создает опросы (polls) и отправляет их в групповой чат с определенным вопросом и вариантами ответов.

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


