import traceback
from envparse import Env
from functions import mess, button, suport
from functions.database import DataBase
from functions.row_request import RowReq, MyBot
from functions.get_meteo import analytics_main
from functions.meteo import add_main


def main():
    env = Env()
    TOKEN = env.str("TOKEN")
    ADMIN_ID = env.str("ADMIN_ID")
    ADMIN_PASSWORD = env.str("ADMIN_PASSWORD")
    row_req = RowReq(token=TOKEN, base_url='https://api.telegram.org')
    bot = MyBot(token=TOKEN, row_req=row_req)
    db = DataBase()

    @bot.message_handler(commands=['start'])
    def start(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        mes = mess.header_mess(message)
        bot.send_message(message.chat.id, mes, parse_mode='html')
        db.add_user(message)

    @bot.message_handler(commands=['days'])
    def show_days(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        markup = button.day_btn()
        bot.send_message(message.chat.id, "Даты обновлены", parse_mode='html', reply_markup=markup)

    @bot.message_handler(regexp=r'Все летные дни!')
    def all_date_fly(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        date_all = button.day_5()
        res = analytics_main(date_all)
        bot.send_message(message.chat.id, mess.repost(res), parse_mode='html')

    @bot.message_handler(regexp=r"[А-Я][а-я]\s\d{2}\s[а-я]+\b")
    def one_day_fly(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        date_f = [mess.re_amdate(message.text)]
        res = analytics_main(date_f)
        bot.send_message(message.chat.id, mess.repost(res, message.text), parse_mode='html')

    @bot.message_handler(commands=['cheng_param'])
    def cheng_param(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        if str(message.chat.id) in ADMIN_PASSWORD:
            message_for_user = mess.cheng_param_mess()
            mes = bot.send_message(message.chat.id, message_for_user, parse_mode='html')
            bot.register_next_step_handler(mes, cheng)

    def cheng(message):
        try:
            lst_command = suport.re_amcommand_change(str(message.text))
            db.cheng_params(*lst_command)
            bot.send_message(message.chat.id, "Изменения добавлены!", parse_mode='html')
        except Exception as err:
            print(err)
            bot.send_message(message.chat.id, "Вы допустили ошибку!", parse_mode='html')

    @bot.message_handler(commands=['dell_spot'])
    def dell_spot_mess(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        if str(message.chat.id) in ADMIN_PASSWORD:
            message_for_user = "Введите название горки, которую собираетесь удвлить"
            mes = bot.send_message(message.chat.id, message_for_user, parse_mode='html')
            bot.register_next_step_handler(mes, dell_spot)
        else:
            bot.send_message(message.chat.id, 'Доступ только для админов!', parse_mode='html')

    def dell_spot(message):
        res = db.dell_spot(message)
        if 'удалена' in res:
            bot.send_message(message.chat.id, 'Обновление прогноза...', parse_mode='html')
            add_main(db.create_new_spot_dict())
            bot.send_message(message.chat.id, res, parse_mode='html')

    @bot.message_handler(commands=['get_spot'])
    def get_spot(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        mes = bot.send_message(message.chat.id, "Введите 'Все' или 'Название горки'", parse_mode='html')
        bot.register_next_step_handler(mes, show_spot)

    def show_spot(message):
        if str(message.text).lower() == 'все':
            bot.send_message(message.chat.id, mess.mess_get_all_spot(db.get_spot()), parse_mode='html')
        else:
            res = mess.mess_get_spot(db.get_spot(str(message.text)))
            bot.send_message(message.chat.id, res, parse_mode='html')

    @bot.message_handler(commands=['add_spot'])
    def create_spot(message):
        print(f'{message.from_user.first_name} - command: {message.text}')
        if str(message.chat.id) in ADMIN_PASSWORD:
            mes = bot.send_message(message.chat.id, mess.step_1(), parse_mode='html')
            bot.register_next_step_handler(mes, add_spot_step)
        else:
            bot.send_message(message.chat.id, 'Доступ только для админов!', parse_mode='html')

    def add_spot_step(message):
        try:
            arg = mess.step_2(str(message.text))
            res_ans = db.add_spot(arg)
            if 'добавлена' in res_ans:
                bot.send_message(message.chat.id, 'Обновление прогноза...', parse_mode='html')
                # add_main(database.create_new_spot_dict())
            bot.send_message(message.chat.id, res_ans, parse_mode='html')
        except IndexError:
            bot.send_message(message.chat.id, f"<b>В данных ошибка или их не достаточно</b>", parse_mode='html')

    while True:
        try:
            bot.polling()
        except Exception as err:
            params = {
                "chat_id": f'{ADMIN_ID}',
                "text": f"{mess.err_mess(err)}\n\n{traceback.format_exc()}"}
            bot.row_req.post(method="sendmessage", params=params)


if __name__ == '__main__':
    main()
