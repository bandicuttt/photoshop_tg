# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from tgbot.data.config import get_admins



def stop_parse():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keyboard.row("❌ Остановить парсинг"),
    return keyboard

def back_to_main_reply():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keyboard.row("◀️ Назад"),
    return keyboard

def main_menu_reply(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in get_admins():
        keyboard.row("👨🏻‍🔧 Панель администратора")
    keyboard.row("👨‍🎨 Создать","🎨 Шаблоны")
    keyboard.row("✨ Избранное",'👨‍💻 Профиль')
    return keyboard