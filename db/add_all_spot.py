
from db import database
from suport_fl.mess import get_lst_spots_from_txt

db = database.DataBase('bot_db.db')


def add_spots():
    with open('spot_list.txt') as file:
        for line in file:
            try:
                line = get_lst_spots_from_txt(line.rstrip())
                db.add_spot(line)
            except IndexError:
                break


if __name__ == '__main__':
    add_spots()
