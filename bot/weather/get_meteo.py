from typing import List
import prettytable as pt
from suport_fl.support import cheng_format_utc as uts, amdate
import datetime


def oneday_meteo(day, j_info):
    timezone = j_info['city']['timezone']
    one_day_meteo = {"city": {"timezone": timezone,
                              "sunrise": j_info['city']['sunrise'],
                              "sunset": j_info['city']['sunset'],
                              "name": j_info['city']['name']},
                     'list': []}
    for day_hour in j_info['list']:
        data_obj = uts(day_hour['dt'], timezone)
        print(data_obj.strftime("%Y-%m-%d"), day)
        if data_obj.strftime("%Y-%m-%d") == day:
            one_day_meteo['list'].append(day_hour)

    return one_day_meteo


def create_text(lst_day: list, meteo_dict, right_now=None):
    str_post = ''

    for day in lst_day:
        if not right_now:
            data = amdate(day)
            meteo = oneday_meteo(day, meteo_dict)
        else:
            data = day
            meteo = meteo_dict
        str_post += f'\n--- <b>{data}</b> ---\n\n'
        str_post += f'<u><b>{meteo["city"]["name"]}</b></u>\n'
        str_post += create_meteo(meteo)

    return str_post


def create_meteo(a):
    timezone = a['city']['timezone']
    lst_header = ['Time', 't', 'Wind', 'Rain', 'Clouds']
    param = []
    for one_hour in a['list']:
        param.append(
            [
                uts(one_hour['dt'], timezone).strftime("%H"),
                int(one_hour['main']['temp']),
                int(one_hour['wind']['speed']),
                int(one_hour['pop'] * 100),
                one_hour['clouds']['all'],
            ]
        )
    table_meteo = create_table(lst_header, param)

    return (
        f'Восход:  {uts(a["city"]["sunrise"], timezone).strftime("%H:%M")}\n'
        f'Закат:  {uts(a["city"]["sunset"], timezone).strftime("%H:%M")}\n\n'
        f'<pre>{table_meteo}</pre>\n'
    )


def create_table(header: list, body: List[List]):
    table_meteo = pt.PrettyTable(header)
    table_meteo.align = 'r'
    for row in body:
        table_meteo.add_row(row)
    return table_meteo

