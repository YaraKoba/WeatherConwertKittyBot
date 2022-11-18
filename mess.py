import datetime
from datetime import date
import re


def header_mess(message):
    return (f'<b>Привет, {message.from_user.first_name}!</b>\n'
            f'Бот позволяет узнать где и когда <b>можно полетать</b>.\n'
            f'Каждый день вы будете получать уведомления о погоде,\n'
            f'чтобы <b>отключить</b> уведомления, введите /stop\n'
            f'чтобы заново <b>включить</b> уведомления, введите /go\n'
            f'<b>Выберете дату, чтобы узнать где полетать</b> &#128526;')


def err_mess(err):
    return f"Type:  {str(type(err))[7:-1]}\n"\
           f"Error:  {err}\n"\
           f"Date:  {datetime.date.today()}"


def repost(all_spot):
    spot_dict = spot_dict = {'kzn': ['Камаево', 'Печищи', 'Услон'],
             'inop': ['Переезд', 'Монастырь', 'Свяга М7', 'Соболевское', 'Макулово', 'Патрикеево'],
             'lai': ['Антоновка', 'Рудник', 'Шуран']}
    for dct in all_spot:
        dat = dct['date']
        str_post = f'<b>{amdate(dat)}</b>\n\n'
        for spot in dct['flydict']:
                str_post += f'<u><b>{spot}</b></u>\n'
                if spot in spot_dict['kzn']:
                    str_post += meteo(dct['kzn'], spot)
                elif spot in spot_dict['inop']:
                    str_post += meteo(dct['inop'], spot)
                elif spot in spot_dict['lai']:
                    str_post += meteo(dct['lai'], spot)
        if len(dct['flydict']) == 0:
            str_post += '<u><b>К сожалению, не летно</b></u> &#128530;\n'
            str_post += meteo(dct['kzn'])
        return str_post


def lam(x):
    return str(round(x, 1))


def meteo(a, spot='Макулово'):
    prognoz = {'Переезд': "https://www.windy.com/55.848/48.510?55.874,48.618,11,m:fefahv0",
               'Монастырь': "https://www.windy.com/55.772/48.660?55.819,48.486,11,m:fd6ahwg",
               'Свяга М7': "https://www.windy.com/55.713/48.600?55.709,48.599,15,m:fd0ahv8",
               'Соболевское': "https://www.windy.com/55.616/48.462?55.521,48.720,10,m:fdQahvV",
               'Макулово': "https://www.windy.com/55.593/48.716?55.617,48.710,12,m:fdOahwm",
               'Патрикеево': "https://www.windy.com/55.467/48.579?55.423,48.579,11,m:fdBahv6",
               'Антоновка': "https://www.windy.com/55.311/49.143?55.266,49.143,11,m:fdmahw3",
               'Рудник': "https://www.windy.com/55.280/49.191?55.271,49.203,14,m:fdiahw8",
               'Шуран': "https://www.windy.com/55.280/49.191?55.369,49.835,13,m:fdrahyc",
               'Камаево': "https://www.windy.com/56.025/49.644?56.021,49.653,14,m:fexahxT",
               'Печищи': "https://www.windy.com/55.776/48.950?55.763,48.983,14,m:fd6ahwJ",
               'Услон': "https://www.windy.com/55.776/48.950?55.763,48.983,14,m:fd6ahwJ",
               'Масловка': "https://www.windy.com/55.439/50.009?55.387,49.922,12,m:fdyahyv",
               'Сорочьи горы': "https://www.windy.com/55.280/49.191?55.369,49.835,13,m:fdrahyc"}
    meteo_dict = {}
    for i in a[0]:
        meteo_dict[i] = []
    for j in a:
        time = int(j["time"][:-3])
        if time == 9 or time == 12 or time == 15:
            for z in j:
                meteo_dict[z] += [j[z]]
    rain = map(lambda x: re.sub(r"(\d\.\d{,2})(.+)", r"\1", str(x)), meteo_dict["rain"])
    return (f'&#127788;  | {" | ".join(list(map(lam, meteo_dict["wind_speed"])))} | м/с\n'
            f'&#127786;  | {" | ".join(list(map(lam, meteo_dict["wind_gust"])))} | м/с\n'
            f'&#129517;  | {" | ".join(list(map(lam, meteo_dict["wind_degree"])))} |°\n'
            f'&#127777;  | {" | ".join(list(map(lam, meteo_dict["temp"])))} | ℃\n'
            f'&#127782;  | {" | ".join(list(rain))} | мм/3ч\n'
            f'<a href="{prognoz[spot]}">Подробнее...</a>\n\n')


def meteo_all(a):
    res_mess = ''
    for i in a:
        temp = int(i["temp"]) if float(i["temp"]) >= 10 or i["temp"] < 0 else ' ' + str(int(i["temp"])) + ' '
        ws = int(i["wind_speed"]) if float(i["wind_speed"]) >= 10 else ' ' + str(int(i["wind_speed"])) + ' '
        wg = int(i["wind_gust"]) if float(i["wind_gust"]) >= 10 else ' ' + str(int(i["wind_gust"])) + ' '
        wdg = i["wind_degree"] if i["wind_degree"] > 100 else ' ' + str(int(i["wind_degree"])) + ' '
        if int(wdg) < 10:
            wdg = ' ' + str(wdg) + ' '
        res_mess += (f'{str(i["time"])[:-2]} | {ws} | {wg} | {wdg} | '
                     f'{temp} | {str(float(i["pop"]))} | {i["rain"]}\n')
    return res_mess


def amdate(dat):
    mon_dct = {'01': 'Января', '02': 'феврыля', '03': 'марта', '04': 'апреля',
           '05': 'майя', '06': 'июня', '07': 'июля', '08': 'августа',
           '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    week_dict = {1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт', 6: 'Сб', 7: 'Вс'}
    new_dat = str(dat).split('-')
    mon = mon_dct[new_dat[1]]
    day = new_dat[2]
    x = map(int, dat.split('-'))
    week = week_dict[datetime.datetime.isoweekday(date(*x))]
    return f'{week} {day} {mon}'


if __name__ == '__main__':
    print(amdate('2022-11-18'))