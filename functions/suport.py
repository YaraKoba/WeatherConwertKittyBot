from datetime import date, datetime
import re


def lam_wind(x):
    res = str(round(float(x), 1))
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
    res = int(round(float(x)))
    if 0 < res < 10:
        res = f'   {res}   '
    elif res >= 10:
        res = f'  {res}  '
    elif 0 > res >= -9:
        res = f'  {res}   '
    elif res <= -10:
        res = f'  {res} '
    return str(res)


def lam_wind_all(x):
    res = str(round(float(x)))
    if len(res) == 1:
        res = f'   {res}   '
    elif len(res) == 2:
        res = f'  {res}  '
    return res


def ampop(m_d):
    pop_time = [tm["time"][1:-3] for tm in m_d if float(tm['pop']) >= 0.4]
    if len(pop_time) > 0:
        return f'Осадки в ({" ".join(pop_time)}) ч'
    else:
        return 'Осадков нет'


def amdegree(dg):
    dg = int(dg)
    if 345 < dg or 15 > dg:
        return '  с  '
    elif 15 <= dg <= 30:
        return 'ссв'
    elif 30 <= dg <= 60:
        return ' св '
    elif 60 <= dg <= 75:
        return 'всв'
    elif 75 <= dg <= 105:
        return '  в  '
    elif 105 <= dg <= 120:
        return ' вюв '
    elif 120 <= dg <= 150:
        return 'юв'
    elif 150 <= dg <= 165:
        return 'ююв'
    elif 165 <= dg <= 195:
        return '  ю  '
    elif 195 <= dg <= 210:
        return 'ююз'
    elif 210 <= dg <= 240:
        return ' юз '
    elif 240 <= dg <= 255:
        return 'зюз'
    elif 255 <= dg <= 285:
        return '  з  '
    elif 285 <= dg <= 300:
        return 'зсз'
    elif 300 <= dg <= 330:
        return ' сз '
    elif 330 <= dg <= 345:
        return 'ссз'


def amdate(dat):
    mon_dct = {'01': 'Января', '02': 'феврыля', '03': 'марта', '04': 'апреля',
               '05': 'майя', '06': 'июня', '07': 'июля', '08': 'августа',
               '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    week_dict = {1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт', 6: 'Сб', 7: 'Вс'}
    new_dat = str(dat).split('-')
    mon = mon_dct[new_dat[1]]
    day = new_dat[2]
    x = map(int, dat.split('-'))
    week = week_dict[datetime.isoweekday(date(*x))]
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
    now = datetime.now()
    year = str(now.year)
    return f'{year}-{mon}-{day}'


def re_amcommand_change(message):
    print(message)
    lst_command = re.findall(r'(\w+?)\s([А-Яа-я.]+?)\s(.+)', message)
    command_dict = {'слева': "wind_degree_l", 'справа': "wind_degree_r", 'с.ш': "lat",
                    'в.д': "lon", 'макс.ветер': "w_max", 'мин.ветер': "w_min",
                    'ссылка': "url", 'описание': "description"}
    return [lst_command[0][0], command_dict[lst_command[0][1]], lst_command[0][2]]