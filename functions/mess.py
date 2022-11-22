import datetime
from datetime import date
from functions.database import get_spot
# from functions.get_meteo import oneday_meteo
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


def repost(all_spot, message=None):
    str_post = ''
    data = ''
    if len(all_spot) == 0:
        str_post += f'\n--- <b>{message}</b> ---\n\n'
        str_post += '<u><b>К сожалению, не летно</b></u> &#128530;\n'
        return str_post
    for dct in all_spot:
        if data != dct['meteo']['date']:
            data = dct['meteo']['date']
            str_post += f'\n--- <b>{amdate(data)}</b> ---\n\n'
        str_post += f'<u><b>{dct["meteo"]["city"]}</b></u>\n'
        str_post += meteo(dct)
    return str_post


def lam_wind(x):
    res = str(round(x, 1))
    if len(res) == 1:
        res = f' {res}.0  '
    elif len(res) == 3:
        res = f' {res}  '
    return res


def lam_degree(x):
    res = str(x)
    if len(res) == 1:
        res = f'  {x}°  '
    elif len(res) == 2:
        res = f'  {x}° '
    elif len(res) == 3:
        res = f' {x}°'
    return res


def lam_temp(x):
    res = int(round(x))
    if 0 < res < 10:
        res = f'   {res}   '
    elif res >= 10:
        res = f'  {res}  '
    elif 0 > x >= -9:
        res = f'  {res}   '
    elif res <= -10:
        res = f'  {res} '
    return res


def meteo(a):
    degree = [(i["win_l"], i["win_r"]) for i in a["fly_time"]]
    fly_hour = [tm['time'][:-2] for tm in a["fly_time"]]
    only_fly_hour = [tm['time'] for tm in a["fly_time"] if tm['wdg'] > 0 and tm['w_s'] > 0]
    hour_point = [str(int((tm['w_s'] + tm['wdg']) * 100)) for tm in a["fly_time"]]
    prognoz = get_spot(a['meteo']['city'])[0][7]
    meteo_dict = {}
    for i in a['meteo']['time'][0]:
        meteo_dict[i] = []
    for j in a['meteo']['time']:
        time = j["time"][:-2]
        if time in fly_hour:
            for z in j:
                meteo_dict[z] += [j[z]]
    rain = map(lambda x: re.sub(r"(\d\.\d{,2})(.+)", r"\1", str(x)), meteo_dict["rain"])
    return (f'Направление ветра:  <b>{degree[0][0]}°-{degree[0][1]}°</b>\n'
            f'<u>Общая оценка: <b>{int((a["time_point"] + a["wind_point"]) * 0.5)}%</b></u>\n'
            f'Оценка ветра:  <b>{a["wind_point"]}%</b>\n'
            f'Летные часы:  <b>{a["time_point"]}%</b> \n({" ".join(only_fly_hour)} )\n'
            f'&#128337;  <u>|  {"  |  ".join(fly_hour)}  | ч</u>\n'
            f'&#127788;  | {" | ".join(list(map(lam_wind, meteo_dict["wind_speed"])))} | м/с\n'
            f'&#127786;  | {" | ".join(list(map(lam_wind, meteo_dict["wind_gust"])))} | м/с\n'
            f'&#129517;  | {" |".join(list(map(lam_degree, meteo_dict["wind_degree"])))} |\n'
            f'&#127777;  | {" | ".join(list(map(lam_temp, meteo_dict["temp"])))} | ℃\n'
            f'&#127782;  |    {"    |    ".join(list(rain))}    | мм/3ч\n'
            f'&#129666;  | {"%  | ".join(hour_point)}%  |\n'
            f'<a href="{prognoz}">Подробнее...</a>\n\n')


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


def re_amdate(dat: str):
    mon_dct = {'01': 'Января', '02': 'феврыля', '03': 'марта', '04': 'апреля',
               '05': 'майя', '06': 'июня', '07': 'июля', '08': 'августа',
               '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    new_dat = str(dat).split(' ')
    mon = ''
    for num in mon_dct:
        if mon_dct[num] == new_dat[2]:
            mon = num
    day = new_dat[1]
    now = datetime.datetime.now()
    year = str(now.year)
    return f'{year}-{mon}-{day}'


def step_1():
    return f'Впишите данные пользуясь шаблоном (писать только то, что в "")\n\n'\
           f'"Название горки" : с.ш"0.0000" : в.д"0.0000" : направление ветра с лева"градусы" : с права"градусы"' \
           f' : минимальный ветре"м/с" : максимальный ветер"м/с" : "ссылка на прогноз" : "описание"\n\n'\
           f'Для поиска координат <a href="https://geotree.ru/coordinates">ссылка</a>'


def step_2(message):
    reg = r'(\w+\b).+?(\d{2}[\.\,]\d{4}).+?(\d{2}[\.\,]\d{4}).+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(https?.+?)\s.+?(\w+.+)'
    return re.findall(reg, message)[0]


def mess_get_spot(arg):
    arg = arg[0]
    return f'<b>Название:</b>  {arg[0]}\n'\
           f'<b>Координаты:</b>  с.ш "{arg[1]}", в.д "{arg[2]}"\n'\
           f'<b>Направление ветра:</b>  {arg[3]}°-{arg[4]}°\n'\
           f'<b>Ветер:</b>  мин - "{arg[5]} м/с", макс - "{arg[6]} м/с"\n'\
           f'<b>Подробный прогноз:</b>  <a href="{arg[7]}">ссылка...</a>\n'\
           f'<b>Описание:</b>  {arg[8]}\n\n'


def mess_get_all_spot(spots):
    res = ''
    k = 0
    spot_sort = sorted([all_inf_spot[0] for all_inf_spot in spots])
    for spot in spot_sort:
        k += 1
        res += f'<b>{k}.</b> {spot}\n'
    return res


if __name__ == '__main__':
    pass
