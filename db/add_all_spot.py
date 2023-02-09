
from db import database
from suport_fl.mess import step_2

db = database.DataBase('bot_db.db')


def add_spots():
    with open('spot_list.txt') as file:
        for line in file:
            try:
                line = step_2(line.rstrip())
                db.add_spot(line)
            except IndexError:
                break


if __name__ == '__main__':
    add_spots()
