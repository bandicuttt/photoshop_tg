# - *- coding: utf- 8 - *-
import configparser

read_config = configparser.ConfigParser()
read_config.read("settings.ini")

BOT_TOKEN = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
BOT_NAME = read_config['settings']['bot_name'].strip().replace("@", "").replace(' ', '')  # имя бота
CHANNEL_LINK = read_config['settings']['channel_url'].strip().replace(" ","") # ссылка на канал
CHAT_LINK = read_config['settings']['chat_url'].strip().replace(" ","") # ссылка на чат
FAQ_LINK = read_config['settings']['faq_url'].strip().replace(" ","") # ссылка на FAQ
LICENCE_LINK = read_config['settings']['licence_url'].strip().replace(" ","") # ссылка на соглашение
PATH_DATABASE = "tgbot/data/database.db"  # Путь к БД
PATH_LOGS = "tgbot/data/logs.log"  # Путь к Логам
BOT_VERSION = "1.0"  # Версия бота


# Получение администраторов бота
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))
    return admins

def get_sub_links():
    read_sub_links = configparser.ConfigParser()
    read_sub_links.read('settings.ini')

    chats =  read_sub_links['settings']['channel_id'].strip().replace(" ", "")

    if "," in chats:
        chats = chats.split(',')
    else:
        if len(chats) >= 1:
            chats = [chats]
        else:
            chats = []

    while "" in chats: chats.remove("")
    while " " in chats: chats.remove(" ")
    while "\r" in chats: chats.remove("\r")
    while "\n" in chats: chats.remove("\n")

    chats = list(map(int, chats))
    return chats


def get_sub_url():
    read_sub_links = configparser.ConfigParser()
    read_sub_links.read('settings.ini')

    chats =  read_sub_links['settings']['channel_url'].strip().replace(" ", "")

    if "," in chats:
        chats = chats.split(',')
    else:
        if len(chats) >= 1:
            chats = [chats]
        else:
            chats = []

    while "" in chats: chats.remove("")
    while " " in chats: chats.remove(" ")
    while "\r" in chats: chats.remove("\r")
    while "\n" in chats: chats.remove("\n")

    chats = list(map(str, chats))
    return chats