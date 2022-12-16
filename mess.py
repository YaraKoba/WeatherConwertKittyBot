from database import DataBase
from suport import *
import re


def header_mess(message):
    return (f'<b>Привет, {message.from_user.first_name}!</b>\n'
            f'Бот позволяет узнать где и когда <b>можно полетать</b>.\n'
            f'Каждый день вы будете получать уведомления о погоде,\n'
            f'чтобы <b>отключить</b> уведомления, введите /stop\n'
            f'чтобы заново <b>включить</b> уведомления, введите /go\n'
            f'<b>Выберете дату, чтобы узнать где полетать</b> &#128526;')


def cheng_param_mess():
    return ('1. Введите название горки.\n'
            '2. Введите один пораметр, который хотите изменить.\n'
            '2.1 Изменяемые пораметры:\n'
            '- "с.ш" или "в.д"\n'
            '- Диапозон ветров "слева" или "справа"\n'
            '- Скорость ветра "мин.ветер" или "макс.ветер"\n'
            '- "cсылка" на прогноз\n'
            '- "описание"\n'
            '3. Новый пораметр\n'
            'Пример: <b>Услон слева 315</b>\n'
            'Еще пример: <b>Переезд описане Это лучшая горка!</b>')

def err_mess(err):
    now = datetime.now()
    return f"Type:  {str(type(err))[7:-1]}\n"\
           f"Error:  {err}\n"\
           f"Date:  {now.strftime('%d-%m-%Y %H:%M')}"


def repost(all_spot, message=None):
    str_post = ''
    data = ''
    if type(all_spot) == dict:
        str_post += f'\n--- <b>{message}</b> ---\n\n'
        str_post += '<u><b>К сожалению, не летно</b></u> &#128530;\n'\
                    f'{meteo_all(all_spot["time"])}'
        return str_post
    for dct in all_spot:
        if data != dct['meteo']['date']:
            data = dct['meteo']['date']
            str_post += f'\n--- <b>{amdate(data)}</b> ---\n\n'
        str_post += f'<u><b>{dct["meteo"]["city"]}</b></u>\n'
        str_post += meteo(dct)
    return str_post


def meteo(a):
    db = DataBase()
    degree = [(i["win_l"], i["win_r"]) for i in a["fly_time"]]
    fly_hour = [tm['time'][:-2] for tm in a["fly_time"]]
    only_fly_hour = [tm['time'] for tm in a["fly_time"] if tm['wdg'] > 0 and tm['w_s'] > 0]
    hour_point = [str(int((tm['w_s'] + tm['wdg']) * 100)) for tm in a["fly_time"]]
    prognoz = db.get_spot(a['meteo']['city'])[0][7]
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
    m_d = {key: [str(tm[key]) for tm in a if int(tm['time'][:-3]) in [9, 15, 18]] for key in a[0]}
    lst_time = [tm[1:-3] for tm in m_d['time']]
    return (f'&#128337;  <u>|{"|".join(list(map(lambda x: f"  {x}  ", lst_time)))}ч</u>\n'
            f'&#127788;  |{"|".join(list(map(lam_wind_all, m_d["wind_speed"])))}м/с\n'
            f'&#127786;  |{"|".join(list(map(lam_wind_all, m_d["wind_gust"])))}м/с\n'
            f'&#129517;  | { " | ".join(list(map(amdegree, m_d["wind_degree"])))}\n'
            f'&#127777;  |{"|".join(list(map(lam_temp, m_d["temp"])))} ℃\n'
            f'&#127782;  {ampop(a)}\n')


def step_1():
    return f'Впишите данные пользуясь шаблоном (писать только то, что в "")\n\n'\
           f'"Название горки" : с.ш"0.0000" : в.д"0.0000" : направление ветра с лева "градусы" : с права"градусы"' \
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
