# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import math

from tgbot.data.config import BOT_NAME, CHANNEL_LINK, CHAT_LINK, FAQ_LINK, LICENCE_LINK, get_sub_url
from tgbot.services.api_sqlite import get_all_layers, get_all_likes, get_templatex

def main_keyboard_menu(user_id=False):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🙇🏻‍♂️Канал', url=CHANNEL_LINK),
                (InlineKeyboardButton(text='💬Чат', url=CHAT_LINK)))
    keyboard.add(InlineKeyboardButton(text='👨🏻‍🏫FAQ', url=FAQ_LINK),
                (InlineKeyboardButton(text='👮Соглашение', url=LICENCE_LINK)))
    keyboard.add(InlineKeyboardButton(text='☑️ Скрыть', callback_data='hide_msg'))
    return keyboard

# def main_keyboard_menu(user_id):
#     keyboard = InlineKeyboardMarkup()
#     keyboard.add(InlineKeyboardButton(text='🎯 Профиль', callback_data='my_profile'))
#     # keyboard.add(InlineKeyboardButton(text='💬 Наш чат', url='https://google.com'))
#     # keyboard.add(InlineKeyboardButton(text='👥 Наш канал', url='t.me/test'))
#     # keyboard.add(InlineKeyboardButton(text="📏 Правила сервиса", url='https://google.com'),
#     #              InlineKeyboardButton(text="🔼 FAQ", url='https://google.com'))
#     keyboard.add(InlineKeyboardButton(text='🚀 Шаблоны', callback_data='choose_country'))

#     if user_id in get_admins():
#         keyboard.add(InlineKeyboardButton(text='🎛 Админ панель', callback_data='admin_panel'))

#     return keyboard

def hide_message_keyboard(text='Cancel'):
    keyboard = InlineKeyboardMarkup()
    if text == 'Cancel':
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))
    if text == 'Hide':
        keyboard.add(InlineKeyboardButton(text='✅ Готово', callback_data='hide_msg'))
    if text == 'Hide_this':
        keyboard.add(InlineKeyboardButton(text='☑️ Скрыть', callback_data='hide_msg'))

    return keyboard

def profile_keyboard_menu():
    keyboard = InlineKeyboardMarkup()
    # keyboard.add(InlineKeyboardButton(text='🔎 Мои шаблоны', callback_data='my_custom_templates'))
    keyboard.add(InlineKeyboardButton(text='📂 Создать шаблон', callback_data='create_my_custom_template'))
    keyboard.add(InlineKeyboardButton(text='⭐️ Избранное', callback_data='my_favorite'))
    keyboard.add(InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main_menu'))
    
    return keyboard


def edit_my_tempalte_keyboard(template_id, show_all=True, remover=0):
    keyboard = InlineKeyboardMarkup()
    if show_all:
        get_categories = get_all_layers(template_id)
        if get_categories:
            if remover >= len(get_categories): remover -= 5
            for count, a in enumerate(range(remover, len(get_categories))):
                if count < 5:
                    keyboard.add(InlineKeyboardButton(get_categories[a]['layer_name'],
                                    callback_data=f"show_layers:{get_categories[a]['layer_id']}:{get_categories[a]['template_id']}"))

            if len(get_categories) <= 5:
                pass
            elif len(get_categories) > 5 and remover < 5:
                keyboard.add(
                    InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                    InlineKeyboardButton("▶️", callback_data=f"next_layers:{remover + 5}:{get_categories[a]['template_id']}"),
                )
            elif remover + 5 >= len(get_categories):
                keyboard.add(
                    InlineKeyboardButton("◀️", callback_data=f"next_layers:{remover - 5}:{get_categories[a]['template_id']}"),
                    InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                )
            else:
                keyboard.add(
                    InlineKeyboardButton("◀️", callback_data=f"next_layers:{remover - 5}:{get_categories[a]['template_id']}"),
                    InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                    InlineKeyboardButton("▶️", callback_data=f"next_layers:{remover + 5}:{get_categories[a]['template_id']}"),
                )

        keyboard.add(InlineKeyboardButton(text='✏️ Добавить слой', callback_data=f'add_new_layer:{template_id}'),
                     InlineKeyboardButton(text='🧩 Добавить QR',callback_data=f'add_new_layer:{template_id}:QR'))

        keyboard.add(InlineKeyboardButton(text='❌ Удалить', callback_data=f'delete_template:{template_id}'),
                     InlineKeyboardButton(text='🖼 Предпросмотр', callback_data=f'prescreem_with_layers:{template_id}:{0}'))
        keyboard.add(InlineKeyboardButton(text='✅ Продолжить', callback_data=f'template_ready:{template_id}'))
    else:
        keyboard.add(InlineKeyboardButton(text='✏️ Добавить слой', callback_data=f'add_new_layer:{template_id}'))
        keyboard.add(InlineKeyboardButton(text='❌ Удалить', callback_data=f'delete_template:{template_id}'))


    return keyboard

def edit_layer_keyboard(layer_id, template_id, align_center, align_right, qr = None):
    data = {1: '🟢', 0: '🔴'}
    keyboard = InlineKeyboardMarkup()
    if not qr:
        keyboard.add(InlineKeyboardButton(text='🏷 Изменить название', callback_data=f'edit_layer:name:{layer_id}'),
                        InlineKeyboardButton(text='🔎 Установить размер шрифта', callback_data=f'edit_layer:font_size:{layer_id}'))

        keyboard.add(InlineKeyboardButton(text='🔤 Изменить шрифт', callback_data=f'edit_layer:font:{layer_id}'),
                        InlineKeyboardButton(text='🌈 Изменить цвет', callback_data=f'edit_layer:color:{layer_id}'))
    if qr:
        keyboard.add(InlineKeyboardButton(text='🔎 Установить размер QR', callback_data=f'edit_layer:font_size:{layer_id}'))

    keyboard.add(InlineKeyboardButton(text='🌐 Изменить координаты', callback_data=f'edit_layer:coordinates:{layer_id}'))
    keyboard.add(InlineKeyboardButton(text=f'{data.get(align_center)} Выравнивание по центру', callback_data=f'change_layer_align:center:{template_id}:{layer_id}'))
    keyboard.add(InlineKeyboardButton(text=f'{data.get(align_right)} Выравнивание по правому краю', callback_data=f'change_layer_align:right:{template_id}:{layer_id}'))

    keyboard.add(InlineKeyboardButton(text='🖼 Предпросмотр', callback_data=f'prescreem_with_layers:{template_id}:{layer_id}'),
                    InlineKeyboardButton(text='❌ Удалить', callback_data=f'delete_layer:{template_id}:{layer_id}'),
                    InlineKeyboardButton(text='✅ Готово', callback_data=f'layer_is_ready:{template_id}:{layer_id}'))

    return keyboard

def use_template_menu(template_id, country_id, category_id, file_name, user_id, fav=None, profile=None):
    count_likes = get_all_likes(template_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🖌 Использовать', callback_data=f'user_use_template:{template_id}:{file_name}'))
    if fav:
        keyboard.add(InlineKeyboardButton(text='🌏 Поделиться', switch_inline_query=f't.me/{BOT_NAME}/?start={template_id}_{file_name}_{country_id}'),
                    InlineKeyboardButton(text='⭐️ Избранное', callback_data=f'add_to_favorite:{template_id}:{country_id}:{category_id}:{file_name}'))
    else:
        keyboard.add(InlineKeyboardButton(text='🌏 Поделиться', switch_inline_query=f't.me/{BOT_NAME}/?start={template_id}_{file_name}_{country_id}'),
                    InlineKeyboardButton(text='⭐️ Избранное', callback_data=f'add_to_favorite:{template_id}:{country_id}:{category_id}:{file_name}'))
    if get_templatex(creator_id=user_id, template_id=template_id):
        keyboard.add(InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'edit_my_template:{template_id}'),
                    (InlineKeyboardButton(text='❌ Удалить', callback_data=f'delete_template:{template_id}')))
    keyboard.add(InlineKeyboardButton(text=f'❤️ {count_likes}', callback_data=f'like_this_template:{template_id}:{country_id}:{category_id}:{file_name}'))
    if profile:
        keyboard.add(InlineKeyboardButton(text='◀️ Назад', callback_data=f'my_profile'))
    else:
        keyboard.add(InlineKeyboardButton(text='◀️ Назад', callback_data=f'show_all_templates_to_drawing:{country_id}:{category_id}'))
    return keyboard


def edit_coordinates_pre_screen_kb(layer_id, width, height):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'✅ Да', callback_data=f'set_coordinates:{layer_id}:{width}:{height}'),
                (InlineKeyboardButton(text=f'❌ Нет', callback_data=f'hide_msg')))
    
    return keyboard


def create_user_template_custom(country_id, category_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'✅ Продолжить', callback_data=f'add_new_template_in_select_category:{country_id}:{category_id}'))
    keyboard.add(InlineKeyboardButton(text=f'❌ Отменить', callback_data=f'hide_msg'))
    return keyboard


def check_template_admin(template_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'✅ Одобрить', callback_data=f'accept_template_admin:{template_id}'))
    keyboard.add(InlineKeyboardButton(text=f'❌ Отклонить', callback_data=f'hide_msg'))
    return keyboard
    

def sub_keyboard():
    keyboard = InlineKeyboardMarkup()
    chats = get_sub_url()
    for chat in chats:
        keyboard.add(InlineKeyboardButton(text=f'🔗 Подписаться', url=chat))
    keyboard.add(InlineKeyboardButton(text=f'✅ Я подписался', callback_data='check_me'))
    return keyboard