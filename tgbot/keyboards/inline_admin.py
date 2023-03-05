# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb


def admin_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    # keyboard.add(ikb(text='🌇 Создать страну', callback_data='add_new_country'))
    # keyboard.add(ikb(text='🗂 Создать категорию', callback_data='add_new_category'))
    # keyboard.add(ikb(text='🖌 Создать шаблон', callback_data='add_new_template'))
    keyboard.add(ikb(text='⬇️ Добавить шрифт', callback_data='add_new_font'))
    keyboard.add(ikb(text='📢 Рассылка', callback_data='spam'))
    keyboard.add(ikb(text='☑️ Скрыть', callback_data='hide_msg'))

    return keyboard


def accept_spam_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='✅ Подтвердить', callback_data='get_file'),
                (ikb(text='❌ Отменить', callback_data='hide_msg')))
    return keyboard

def add_file_to_spam():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='✅ Да', callback_data='add_file:True'),
                (ikb(text='❌ Нет', callback_data='add_file:False')))
    return keyboard

def accept_spam():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(ikb(text='✅ Да', callback_data='accept_spam'),
                (ikb(text='❌ Нет', callback_data='hide_msg')))
    return keyboard