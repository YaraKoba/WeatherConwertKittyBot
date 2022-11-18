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
        # c.execute("""CREATE TABLE usr_data (
        #     usr_name text,
        #     usr_sname text,
        #     chat_id integer
        # )""")
        c.execute("INSERT INTO usr_data VALUES (?, ?, ?)",
                  (message.from_user.first_name, message.from_user.last_name, message.chat.id))
        # c.execute("DELETE FROM usr_data WHERE rowid > 2")
        c.execute("SELECT * FROM usr_data")
        print(c.fetchall())
        db.commit()


def get_weather():
    with open('weather.json', 'r') as file:
        j_meteo = json.load(file)
    return j_meteo