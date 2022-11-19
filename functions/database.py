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
            except:
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
        c.execute("INSERT INTO usr_data VALUES (?, ?, ?, 'Yes')",
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
        c.execute("INSERT INTO spot_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7], arg[8]))
        db.commit()


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


def dell_spot(spot_name):
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


def get_weather():
    with open('weather.json', 'r') as file:
        j_meteo = json.load(file)
    return j_meteo


if __name__ == '__main__':
    # add_spot(('Услон', '55.8176', '48.4749', '345', '15', '4', '10', 'https://www.windy.com/55.848/48.510?55.874,48.618,11,m:fefahv0', 'хорошая горка'))
    print(get_spot('Услон'))

