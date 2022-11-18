from database import get_weather
from mess import repost
import re


def go_fly(lst_d: list):
    try:
        city_dict = get_weather()
        total_lst = []
        for d in lst_d:
            lst_city = []
            for city in city_dict:
                lst_city += [get_meteo(d[:-3], city_dict[city], city)]
            if len(lst_d) == 5:
                if len(searchflay(lst_city)['flydict']) != 0:
                    total_lst += [searchflay(lst_city)]
            else:
                total_lst += [searchflay(lst_city)]
        return repost(total_lst)
    except IndexError:
        print('Прогноз пока не обновился')


def get_meteo(day, j_info, city):
    reg = r'(\d{4})(.)(\d{2})(.)(\d{2})(\s.{5})(.+)'
    oneday_dict = {'city': city, 'date': day, 'time': []}
    for n in j_info['list']:
        day_hour = n
        data = re.sub(reg, r'\5\2\3\4\1', day_hour['dt_txt'])
        if day_hour['dt_txt'][:-9] == day:
            time_data = re.sub(reg, r'\6', day_hour['dt_txt'])
            temp = day_hour['main']['temp']
            wind_speed = day_hour['wind']['speed']
            wind_gust = day_hour['wind']['gust']
            wind_degree = day_hour['wind']['deg']
            pop = day_hour['pop']
            try:
                rain = day_hour['rain']['3h']
            except KeyError:
                rain = 0
            oneday_dict['time'] += [{'time': time_data, 'temp': temp, 'wind_speed': wind_speed, 'wind_gust': wind_gust,
                                     'wind_degree': wind_degree, 'pop': pop, 'rain': rain}]
            if time_data == '21:00':
                break

    return oneday_dict


def coolday(md, city):
    time_1 = md['time']
    pop = md['pop']
    rain = md['rain']
    wg = md['wind_gust']
    ws = md['wind_speed']
    wdg = md['wind_degree']
    lst = []

    # print(f'time = {time_1}')
    # print(f'pop = {pop}')
    # print(f'rain = {rain}')
    # print(f'wg = {wg}')
    # print(f'ws = {ws}')
    # print(f'wdg = {wdg}')

    if pop > 0.6 or rain > 0.6 or wg > 9 or (wg - ws) > 7:
        return False
    if (345 <= wdg <= 360 or 0 <= wdg <= 15) and wg > 5 and city == 'Инополис':
        lst += ['Переезд']
    if (270 <= wdg <= 330) and wg > 5 and city == 'Инополис':
        lst += ['Монастырь']
    if (270 <= wdg <= 325) and wg > 5 and city == 'Инополис':
        lst += ['Свияга М7']
    if (315 <= wdg <= 360 or 0 <= wdg <= 45 or 135 <= wdg <= 225) and city == 'Инополис':
        lst += ['Соболевское']
    if (250 <= wdg <= 275) and wg > 5 and city == 'Инополис':
        lst += ['Макулово']
    if (230 <= wdg <= 255) and wg > 5 and city == 'Инополис':
        lst += ['Патрикеево']
    if (0 <= wdg <= 45) and wg > 5 and city == 'Казань':
        lst += ['Услон']
    if (0 <= wdg <= 25 or 345 <= wdg <= 0) and wg > 3 and city == 'Казань':
        lst += ['Печищи']
    if (40 <= wdg <= 90 or 120 <= wdg <= 150) and wg > 5 and city == 'Казань':
        lst += ['Камаево']
    if (75 <= wdg <= 95) and wg > 5 and city == 'Лаишево':
        lst += ['Антоновка']
    if (65 <= wdg <= 90) and wg > 3 and city == 'Лаишево':
        lst += ['Рудник']
    if (200 <= wdg <= 240) and wg > 5 and city == 'Лаишево':
        lst += ['Шуран']
    if (130 <= wdg <= 170) and wg > 5 and city == 'Лаишево':
        lst += ['Сорочьи горы']
    if (80 <= wdg <= 120) and wg > 5 and city == 'Лаишево':
        lst += ['Масловка']
    return lst


def searchflay(lst_city):
    flydict = {'Переезд': 0, 'Монастырь': 0, 'Патрикеево': 0,
               'Свияга М7': 0, 'Услон': 0, 'Соболевское': 0, 'Макулово': 0,
               'Антоновка': 0, 'Рудник': 0, 'Шуран': 0, 'Камаево': 0, 'Сорочьи горы': 0, 'Масловка': 0}
    fly_res = {'date': '', 'flydict': [], 'kzn': lst_city[0]['time'],
               'inop': lst_city[1]['time'], 'lai': lst_city[2]['time']}
    fly_res['date'] = lst_city[0]['date']
    data = fly_res['date']
    # print(f'data = {data}')
    for pl in lst_city:
        for tm in pl['time']:
            x = coolday(tm, pl['city'])
            if x:
                for i in x:
                    flydict[i] += 1
    for n in flydict:
        if flydict[n] >= 3:
            fly_res['flydict'] += [n]
    return fly_res


if __name__ == '__main__':
    print(repost(go_fly(['2022-11-20 Вт'])))