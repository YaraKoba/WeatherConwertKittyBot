
from suport_fl.suport import *
import prettytable as pt
import re


def header_mess(message):
    return (f'<b>Привет, {message.from_user.first_name}!</b>\n'
            f'Бот позволяет узнать где и когда <b>можно полетать</b>.\n'
            f'Каждый день вы будете получать уведомления о погоде,\n'
            f'<b>Команды:</b>\n/stop - <b>отключить</b> уведомления\n'
            f'/go - <b>включить</b> уведомления\n'
            f'/days - обновить дни\n'
            f'/get_spot - Посмотреть добавленные горки\n\n'
            f'<b>Обозначения в прогнозе:</b>\n'
            f'Time - Время в часах\n'
            f't°C - Температура воздуха\n'
            f'm/s - Скорость ветра\n'
            f'M/S - Порывы ветра\n'
            f'Dg° - Направление ветра\n'
            f'V% - Оценка погодных условий (Сила и Направление ветра)\n\n'
            f'<b>Нажмите на дату, чтобы узнать где полетать</b> &#128526;')


def cheng_param_mess():
    return ('1. Введите название горки.\n'
            '2. Введите один параметр, который хотите изменить.\n'
            '2.1 Изменяемые параметры:\n'
            '- "с.ш" или "в.д"\n'
            '- Диапозон ветров "слева" или "справа"\n'
            '- Скорость ветра "мин.ветер" или "макс.ветер"\n'
            '- "cсылка" на прогноз\n'
            '- "описание"\n'
            '3. Новый параметр\n'
            'Пример: <b>Услон слева 315</b>\n'
            'Еще пример: <b>Переезд описане Это лучшая горка!</b>')


def err_mess(err):
    now = datetime.now()
    return f"Type:  {str(type(err))[7:-1]}\n"\
           f"Error:  {err}\n"\
           f"Date:  {now.strftime('%d-%m-%Y %H:%M')}"


def repost(all_spot, spots, d):
    str_post = ''
    data = ''

    if type(all_spot) == dict:
        message = amdate(d[0]) if len(d) == 1 else 'В ближайшие 5 дней'
        str_post += f'\n--- <b>{message}</b> ---\n\n'
        str_post += '<u><b>Летная погода не найдена</b></u> &#128530;\n'\
                    f'{easy_meteo(all_spot["time"])}'
        return str_post

    for dct in all_spot:
        if data != dct['meteo']['date']:
            data = dct['meteo']['date']
            str_post += f'\n--- <b>{amdate(data)}</b> ---\n\n'
        str_post += f'<u><b>{dct["meteo"]["city"]}</b></u>\n'
        str_post += meteo(dct, spots)

    return str_post


def meteo(a, spots):
    sp_dc = {}
    for sp in spots:
        if sp['name'] == a['meteo']['city']:
            sp_dc = sp
            break

    degree = [(i["win_l"], i["win_r"]) for i in a["fly_time"]]
    fly_hour = [tm['time'][:-2] for tm in a["fly_time"]]
    only_fly_hour = [tm['time'] for tm in a["fly_time"] if tm['wdg'] > 0 and tm['w_s'] > 0]
    prognoz = sp_dc['url_forecast']
    fly_meteo = []

    for j in a['meteo']['time']:
        time = j["time"][:-2]
        if time in fly_hour:
            fly_meteo += [j]

    lst_header = ['Час', 'Вет', 'Пор', 'Н', 'Вер']
    point = (str(int((tm['w_s'] + tm['wdg']) * 100)) for tm in a["fly_time"])

    table_meteo = pt.PrettyTable(lst_header)
    table_meteo.align = 'r'
    table_meteo.align['time'] = 'l'

    while fly_meteo:
        one_hour = fly_meteo.pop(0)
        time = one_hour["time"][1:-3]
        w_s, w_g = list(map(lam_wind_all, [one_hour["wind_speed"], one_hour["wind_gust"]]))
        wdg = one_hour["wind_degree"]
        v = next(point)
        table_meteo.add_row([time, w_s, w_g, wdg, v])

    return (f'Направление ветра:  <b>{degree[0][0]}°-{degree[0][1]}°</b>\n'
            f'<u>Общая оценка: <b>{int((a["time_point"] + a["wind_point"]) * 0.5)}%</b></u>\n'
            f'Оценка ветра:  <b>{a["wind_point"]}%</b>\n'
            f'Летные часы:  <b>{a["time_point"]}%</b> \n({" ".join(only_fly_hour)} )\n'
            f'<pre>{table_meteo}</pre>\n&#127782;  {ampop(a["meteo"]["time"])}\n'
            f'<a href="{prognoz}">Подробнее...</a>\n\n')


def easy_meteo(a):
    dict_img = {"wind_speed": 'm/s', "wind_gust": 'M/S', "wind_degree": 'Dg°', "temp": 't°C'}
    m_d = {key: [str(tm[key]) for tm in a if int(tm['time'][:-3]) in [9, 15, 18]] for key in a[1]}
    lst_time = ['Time'] + [tm[1:-3] for tm in m_d['time']]
    table_meteo = pt.PrettyTable(lst_time)
    table_meteo.align = 'r'
    table_meteo.align['Time'] = 'l'
    for key in m_d:
        if key not in ['time', 'pop', 'rain']:
            if key in ["wind_speed", "wind_gust"]: m_d[key] = list(map(lam_wind_all, m_d[key]))
            if key in ["temp"]: m_d[key] = list(map(lam_temp, m_d[key]))
            if key in ["wind_degree"]: m_d[key] = list(map(amdegree, m_d[key]))
            row = [dict_img[key]] + m_d[key]
            table_meteo.add_row(row)
    return f'<pre>{table_meteo}</pre>\n&#127782;  {ampop(a)}\n'


def step_1():
    return f'Впишите данные пользуясь шаблоном (писать только то, что в "")\n\n'\
           f'"Название горки" : с.ш"0.0000" : в.д"0.0000" : направление ветра с лева "градусы" : с права"градусы"' \
           f' : минимальный ветре"м/с" : максимальный ветер"м/с" : "ссылка на прогноз" : "описание"\n\n'\
           f'Для поиска координат <a href="https://geotree.ru/coordinates">ссылка</a>'


def step_2(message):
    reg = r'(\w+\b).+?(\d{2}[\.\,]\d{4}).+?(\d{2}[\.\,]\d{4}).+?(\d+).+?(\d+).+?(\d+).+?(\d+).+?(https?.+?)\s.+?(\w+.+)'
    return re.findall(reg, message)[0]


def mess_get_spot(spot_dict):
    return f'\n\n<b>Название:</b>  {spot_dict["name"]}\n'\
           f'<b>Координаты:</b>  с.ш "{spot_dict["lat"][:7]}", в.д "{spot_dict["lon"][:7]}"\n'\
           f'<b>Направление ветра:</b>  {spot_dict["wind_degree_l"]}°-{spot_dict["wind_degree_r"]}°\n'\
           f'<b>Ветер:</b>  мин - "{spot_dict["wind_min"]} м/с", макс - "{spot_dict["wind_max"]} м/с"\n\n' \
           f'<b><a href="{spot_dict["url_forecast"]}">Windy прогноз</a></b>\n' \
           f'<b><a href="{spot_dict["url_map"]}">Google map</a></b>  \n\n' \
           f'<b>Описание:</b>  {spot_dict["description"]}\n\n\n\n'


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
