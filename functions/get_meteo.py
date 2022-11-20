from functions.database import get_weather, get_spot
from button import cheng_format_utc as uts
import re


def go_fly(lst_d: list):
    try:
        city_dict = get_weather('weather.json')
        total_lst = []
        for d in lst_d:
            lst_city = []
            for city in city_dict:
                lst_city += [oneday_meteo(d, city_dict[city], city)]
            if len(lst_d) == 5:
                if len(searchflay(lst_city)['flydict']) != 0:
                    total_lst += [searchflay(lst_city)]
            else:
                total_lst += [searchflay(lst_city)]
        return total_lst
    except IndexError:
        print('Прогноз пока не обновился')


def oneday_meteo(day, j_info, city):
    reg = r'(\d{4})(.)(\d{2})(.)(\d{2})(\s.{5})(.+)'
    sun_up = j_info['city']['sunrise']
    sun_down = j_info['city']['sunset']
    oneday_dict = {'city': city, 'date': day, 'sun_up': sun_up, 'sun_down': sun_down, 'time': []}
    for n in j_info['list']:
        day_hour = n
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
        lst += ['Свияга_М7']
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
        lst += ['Камаево_юв']
        lst += ['Камаево_св']
    if (75 <= wdg <= 95) and wg > 5 and city == 'Лаишево':
        lst += ['Антоновка']
    if (65 <= wdg <= 90) and wg > 3 and city == 'Лаишево':
        lst += ['Рудник']
    if (200 <= wdg <= 240) and wg > 5 and city == 'Лаишево':
        lst += ['Шуран']
    if (130 <= wdg <= 170) and wg > 5 and city == 'Лаишево':
        lst += ['Сорочьи_горы']
    if (80 <= wdg <= 120) and wg > 5 and city == 'Лаишево':
        lst += ['Масловка']
    return lst


def searchflay(lst_city):
    flydict = {'Переезд': 0, 'Монастырь': 0, 'Патрикеево': 0,
               'Свияга_М7': 0, 'Услон': 0, 'Соболевское': 0, 'Макулово': 0,
               'Антоновка': 0, 'Рудник': 0, 'Шуран': 0, 'Камаево_юв': 0, 'Камаево_св': 0, 'Сорочьи_горы': 0, 'Масловка': 0}
    fly_res = {'date': '', 'flydict': [], 'kzn': lst_city[0]['time'],
               'inop': lst_city[1]['time'], 'lai': lst_city[2]['time']}
    fly_res['date'] = lst_city[0]['date']
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


def analytics_main(lst_day: list):  # add_point_to_spot(oneday_meteo('2022-11-22', spot_dict['Масловка'], 'Масловка'))
    spot_dict = get_weather('spot_weather.json')
    meteo_all_days = [oneday_meteo(one_day, spot_dict[spot], spot) for one_day in lst_day for spot in spot_dict]
    total_res = [add_point_to_spot(one_day) for one_day in meteo_all_days if add_point_to_spot(one_day)['point'] > 0]
    return total_res


def add_point_to_spot(meteo_one_days):
    spot = meteo_one_days['city']
    sun_up = uts(meteo_one_days['sun_up'])[11:-3]
    sun_down = uts(meteo_one_days['sun_down'])[11:-3]
    one_day_points = [get_point(tree_h, spot) for tree_h in meteo_one_days['time']]
    return analytics_data_point(one_day_points, spot, meteo_one_days['date'], sun_up, sun_down)


def analytics_data_point(o_d_p, spot, date, sun_up, sun_down):
    int_up = int(sun_up[:-3])
    int_down = int(sun_down[:-3])
    sort_hours = [t_h for t_h in o_d_p if t_h['wdg'] > 0 and t_h['w_s'] > 0
                  and int_up - 1 <= int(t_h['time'][:-3]) <= int_down + 1]
    try:
        point_fly_time = int(len(sort_hours) / 4 * 50)
        point_ws_wdg = int(sum([(point['w_s'] + point['wdg']) for point in sort_hours]) / len(sort_hours) * 50)
    except ZeroDivisionError:
        point_ws_wdg, point_fly_time = 0, 0
    result = {'spot': spot, 'date': date, 'sun_up': sun_up, 'sun_down': sun_down,
              'point': point_ws_wdg + point_fly_time}
    return result


def get_point(m_t, spot):
    pop = m_t['pop']
    rain = m_t['rain']
    w_g = m_t['wind_gust']
    w_s = m_t['wind_speed']
    wdg = m_t['wind_degree']
    wdg_l = int(get_spot(spot)[0][3])
    wdg_r = int(get_spot(spot)[0][4])
    w_min = int(get_spot(spot)[0][5])
    w_max = int(get_spot(spot)[0][6])
    point_dict = {'time': m_t['time'], 'wdg': 0, 'w_s': 0}
    if pop < 0.6 and rain < 0.6 and w_g < 10 and (w_g - w_s) < 7:
        if wdg_l < wdg_r:
            if wdg_l + middle(wdg_l, wdg_r) - 5 <= wdg <= wdg_r + middle(wdg_l, wdg_r) + 5:
                point_dict['wdg'] += 0.25
            if wdg_l <= wdg <= wdg_r:
                point_dict['wdg'] += 0.25
        else:
            if mid_wdg_h(wdg_l, wdg, wdg_r):
                point_dict['wdg'] += 0.25
            if wdg_l <= wdg or wdg_r >= wdg:
                point_dict['wdg'] += 0.25
        if w_min + middle(w_min, w_max) <= w_g <= w_min + middle(w_min, w_max) + 2:
            point_dict['w_s'] += 0.25
        if w_min < w_g <= w_max:
            point_dict['w_s'] += 0.25
    return point_dict


def middle(mn, mx):
    return (mx - mn) / 2


def mid_wdg_h(lef, w, r):
    mid = ((360 - lef) + r) / 2
    if lef + mid - 5 > 360 and r - mid + 5 < 0:
        if lef + mid - 5 - 360 <= w <= lef + mid + 5 - 360:
            return True
    elif lef + mid - 5 < 360 and r - mid + 5 > 0:
        if lef + mid - 5 <= w or r - mid + 5 >= w:
            return True
    else:
        if lef + mid - 5 <= w <= lef + mid + 5:
            return True


if __name__ == '__main__':
    pass
    # for i in analytics_main(['2022-11-20', '2022-11-22', '2022-11-23', '2022-11-24', '2022-11-25']):
    #     print(i)
    # spot_dict = get_weather('spot_weather.json')
    # print(add_point_to_spot(oneday_meteo('2022-11-22', spot_dict['Монастырь'], 'Монастырь')))
