import telebot
from config import TOKEN
from telebot import types
from toNameCheckData import ukrainianAlphas
import os
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()


bot = telebot.TeleBot(TOKEN)

def user_name_check(message):
    name_list = message.text.lower().split()
    if len(name_list) == 3:
        global name_str
        name_list = list(map(lambda el: el.capitalize(), name_list))

        user_name_confirm = True

        for el in name_list:
            letter_list = list(map(lambda letter: letter.lower() in ukrainianAlphas, el))
            if not all(letter_list):
                user_name_confirm = False

        if user_name_confirm:
            bot.send_message(message.chat.id, '✅Чудово, ім\'я введено!')
            name_str = ' '.join(name_list)

            if os.path.exists(f'newStudents/{name_str}'):
                os.rmdir(f'newStudents/{name_str}')

            os.mkdir(f'newStudents/{name_str}')

            user_email_input(message)
        else:
            example_name = 'Іванов Іван Іванович'
            user_name_retry = bot.send_message(message.chat.id,
                                               text=f'❌Упс, сталася помилка! <b>{message.from_user.first_name}</b>, введіть <b>повне ім\'я (ПІБ) коректно</b>:\n<i>Приклад повного імені: {example_name}</i>', parse_mode='html')
            bot.register_next_step_handler(user_name_retry, user_name_check)

    else:
        example_name = 'Іванов Іван Іванович'
        user_name_retry = bot.send_message(message.chat.id, text=f'❌Упс, сталася помилка! <b>{message.from_user.first_name}</b>, введіть <b>повне ім\'я (ПІБ) коректно</b>:\n<i>Приклад повного імені: {example_name}</i>', parse_mode='html')
        bot.register_next_step_handler(user_name_retry, user_name_check)


def user_email_check(message):
    global user_email

    user_email = message.text
    user_email_confirm = True

    if '@' not in user_email or '.' not in user_email:
        user_email_confirm = False

    if not user_email_confirm:
        example_email = 'mail@gmail.com'
        user_email = bot.send_message(message.chat.id,
                                      text=f'❌Упс, сталася помилка! <b>{message.from_user.first_name}</b>, введіть, будь ласка, Вашу <b>електронну пошту коректно</b>:\n'
                                           f'<i>Приклад електронної пошти: {example_email}</i>', parse_mode='html')
        bot.register_next_step_handler(user_email, user_email_check)
    else:
        if registered_email_check(user_email):
            bot.send_message(message.chat.id, f'❌<b>{message.from_user.first_name}</b>, Ваша електронна адреса вже зареєстрована', parse_mode='html')
            example_email = 'mail@gmail.com'
            user_email = bot.send_message(message.chat.id,
                                          text=f'❌Упс, сталася помилка! <b>{message.from_user.first_name}</b>, введіть, будь ласка, Вашу <b>електронну пошту коректно</b>:\n'
                                               f'<i>Приклад електронної пошти: {example_email}</i>', parse_mode='html')
            bot.register_next_step_handler(user_email, user_email_check)
        else:
            user_email_add(user_email)
            dir_rename()
            bot.send_message(message.chat.id, '✅Чудово, електронну пошту введено!')

def user_email_add(email):
    with open('registedUsers/registeredUsersEmail.txt', 'a', encoding='utf-8') as registered_file:
        print(email, file=registered_file)

def registered_email_check(email):

    with open('registedUsers/registeredUsersEmail.txt', 'r', encoding='utf-8') as registered_file:
        if email in registered_file.readlines():
            return True
        return False

def dir_rename():
    os.rename(f'newStudents/{name_str}', f'newStudents/{name_str + " " + user_email}')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Новий учень👨‍🎓')
    btn2 = types.KeyboardButton('Вже навчаюсь🚘')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text=f'👋<b>Автошкола \"City Driving School\"</b> вітає Вас, <b>{message.from_user.first_name}</b>!'
                                           f'\n🙏Оберіть, будь ласка, ваш статус:', reply_markup=markup, parse_mode='html')

@bot.message_handler(func=lambda message: message.text == 'Новий учень👨‍🎓')
def new_user(message):
    example_name = 'Іванов Іван Іванович'
    user_name = bot.send_message(message.chat.id, text=f'<b>{message.from_user.first_name}</b>, для того, щоб стати нашим учнем введіть Ваше <b>повне ім\'я (ПІБ)</b>:'
                                                       f'\n<i>Приклад повного імені: {example_name}</i>', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    bot.register_next_step_handler(user_name, user_name_check)

@bot.message_handler(func=lambda message: message.text == 'Новий формат🪪')
def new_format_id_upload(message):
    bot.send_message(message.chat.id, text=f'🪪<b>{message.from_user.first_name}</b>, надішліть, будь ласка, фото Вашої <b>ID-картки</b>'
                                           f'\n❗<b><i>З ДВОХ СТОРІН</i></b>❗', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')


def user_email_input(message):
    example_email = 'mail@gmail.com'
    user_email = bot.send_message(message.chat.id, text=f'<b>{message.from_user.first_name}</b>, введіть, будь ласка, вашу електронну пошту:\n'
                                                        f'<i>Приклад електронної пошти: {example_email}</i>', parse_mode='html')
    bot.register_next_step_handler(user_email, user_email_check)

def user_documents_input(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_id_type_new = types.KeyboardButton('Новий формат🪪')
    btn_id_type_old = types.KeyboardButton('Старий формат📖')
    markup.add(btn_id_type_new, btn_id_type_old)
    bot.send_message(message.chat.id, text=f'<b>{message.from_user.first_name}</b>, оберіть формат Вашого паспорту:\n'
                                           f'<i>\"Новий формат\" -> ID-картка\n'
                                           f'\"Старий формат\" -> паспорт-книжка</i>', parse_mode='html', reply_markup=markup)

bot.polling(True)




