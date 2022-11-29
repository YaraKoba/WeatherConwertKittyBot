import json
import sqlite3


def pull_chat_id():
    res_lst = []
    with sqlite3.connect("bot_db.db") as db:
        c = db.cursor()
        c.execute("SELECT * FROM usr_data")
        item = c.fetchall()
        for el in item:
            try:
                res_lst += [el[2]]
            except Exception as err:
                print(err)
                c.execute("DELETE FROM usr_data WHERE chat_id=?", (el[2],))
    return res_lst


def add_user(message):
    with sqlite3.connect("bot_db.db") as db:
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS usr_data (
            usr_name text,
            usr_sname text,
            chat_id integer,
            reminder text
        )""")
        c.execute("SELECT * FROM usr_data")
        item = c.fetchall()
        for el in item:
            if el[2] == message.chat.id:
                return False
        c.execute("INSERT INTO usr_data VALUES (?, ?, ?)",
                  (message.from_user.first_name, message.from_user.last_name, message.chat.id))
        c.execute("SELECT * FROM usr_data")
        item = c.fetchall()
        print(item)
        # c.execute("DELETE FROM usr_data WHERE rowid > 2")
        db.commit()


def add_spot(arg):
    with sqlite3.connect("bot_db.db") as db:
        c = db.cursor()
        # c.execute("DROP TABLE spot_data")
        c.execute("""CREATE TABLE IF NOT EXISTS spot_data (
                    spot_name text,
                    lat text,
                    lon text,
                    wind_degree_l text,
                    wind_degree_r text,
                    w_min text,
                    w_max text,
                    url text,
                    description text
                )""")
        c.execute(f"SELECT spot_name FROM spot_data")
        iter = [spot[0] for spot in c.fetchall()]
        if arg[0] not in iter:
            c.execute("INSERT INTO spot_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7], arg[8]))
            db.commit()
            return f"Горка: '{arg[0]}', добавлена"
        else:
            return 'Горка уже длбавлена'


def get_spot(spot_name=None):
    with sqlite3.connect("bot_db.db") as db:
        c = db.cursor()
        # c.execute("DELETE FROM spot_data")
        if spot_name:
            c.execute(f"SELECT * FROM spot_data WHERE spot_name = '%s'" % (spot_name, ))
        else:
            c.execute(f"SELECT * FROM spot_data")
        item = c.fetchall()
        db.commit()
        return item


def dell_spot(message):
    spot_name = str(message.text)
    with sqlite3.connect("bot_db.db") as db:
        c = db.cursor()
        c.execute("SELECT * FROM spot_data")
        item = c.fetchall()
        for el in item:
            if el[0] == spot_name:
                c.execute("DELETE FROM spot_data WHERE spot_name = '%s'" % (spot_name, ))
                db.commit()
                return f'Горка "{spot_name}" удалена'
        return f'Горка "{spot_name}" не найдена'


def create_new_spot_dict():
    fly_spot = [spot[0] for spot in get_spot()]
    new_spot_dict = {spot: get_spot_lat_lon(spot)[0] for spot in fly_spot}
    return new_spot_dict


def get_spot_lat_lon(spot_name):
    with sqlite3.connect("bot_db.db") as db:
        c = db.cursor()
        if spot_name:
            c.execute(f"SELECT lat, lon FROM spot_data WHERE spot_name = '%s'" % (spot_name, ))
        item = c.fetchall()
        db.commit()
        return item


def get_weather(name_file):
    with open(f'{name_file}', 'r') as fi:
        j_meteo = json.load(fi)
    return j_meteo


if __name__ == '__main__':
    print(get_spot_lat_lon('Услон'))
