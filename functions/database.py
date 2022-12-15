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
                res_lst += [(el[2], el[3])]
            except Exception as err:
                print(err)
                c.execute("DELETE FROM usr_data WHERE chat_id=?", (el[2],))
    return res_lst


class DataBase:
    def __init__(self, file_name='bot_db.db'):
        self.db = sqlite3.connect(file_name, check_same_thread=False)
        self.c = self.db.cursor()

    def get_spot(self, spot_name=None):
        if spot_name:
            self.c.execute(f"SELECT * FROM spot_data WHERE spot_name = '%s'" % (spot_name,))
        else:
            self.c.execute(f"SELECT * FROM spot_data")
        item = self.c.fetchall()
        self.db.commit()
        return item

    def cheng_params(self, spot, param, mes):
        sql = f"UPDATE spot_data SET {param} = ? WHERE spot_name = ?"
        self.c.execute(sql, (mes, spot))
        self.db.commit()

    def add_spot(self, arg):
        self.c.execute("""CREATE TABLE IF NOT EXISTS spot_data (
                            spot_name text UNIQUE,
                            lat text,
                            lon text,
                            wind_degree_l text,
                            wind_degree_r text,
                            w_min text,
                            w_max text,
                            url text,
                            description text
                        )""")
        self.c.execute(f"SELECT spot_name FROM spot_data")
        iter = [spot[0] for spot in self.c.fetchall()]
        if arg[0] not in iter:
            self.c.execute("INSERT INTO spot_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7], arg[8]))
            self.db.commit()
            return f"Горка: '{arg[0]}', добавлена"
        else:
            return 'Горка уже длбавлена'

    def dell_spot(self, message):
        spot_name = message
        self.c.execute("SELECT * FROM spot_data")
        item = self.c.fetchall()
        for el in item:
            if el[0] == spot_name:
                self.c.execute("DELETE FROM spot_data WHERE spot_name = '%s'" % (spot_name,))
                self.db.commit()
                return f'Горка "{spot_name}" удалена'
        return f'Горка "{spot_name}" не найдена'

    def add_user(self, message):
        self.c.execute("""CREATE TABLE IF NOT EXISTS usr_data (
            usr_name text,
            usr_sname text,
            chat_id integer,
            reminder text
        )""")
        self.c.execute("SELECT * FROM usr_data")
        item = self.c.fetchall()
        for el in item:
            if el[2] == message.chat.id:
                return False
        self.c.execute("INSERT INTO usr_data VALUES (?, ?, ?, ?)",
                       (message.from_user.first_name, message.from_user.last_name, message.chat.id, 'Yes'))
        self.c.execute("SELECT * FROM usr_data")
        item = self.c.fetchall()
        print(item)
        # self.c.execute("DELETE FROM usr_data WHERE rowid > 2")
        self.db.commit()

    def get_spot_lat_lon(self, spot_name):
        c = self.db.cursor()
        if spot_name:
            c.execute(f"SELECT lat, lon FROM spot_data WHERE spot_name = '%s'" % (spot_name,))
        item = c.fetchall()
        self.db.commit()
        return item

    def create_new_spot_dict(self):
        fly_spot = [spot[0] for spot in self.get_spot()]
        new_spot_dict = {spot: self.get_spot_lat_lon(spot)[0] for spot in fly_spot}
        return new_spot_dict

    def remainder_client(self, command, chat_id):
        sql = f"UPDATE usr_data SET reminder='{command}' WHERE chat_id={chat_id}"
        self.db.execute(sql)
        self.db.commit()


def get_weather(name_file='spot_weather.json'):
    with open(f'{name_file}', 'r') as fi:
        j_meteo = json.load(fi)
    return j_meteo


if __name__ == '__main__':
    n = DataBase()
    print(n.get_spot_lat_lon('Услон'))
