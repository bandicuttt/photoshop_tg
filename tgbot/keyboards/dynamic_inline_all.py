# - *- coding: utf- 8 - *-
import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.api_sqlite import get_all_countries, get_all_categories_with_country_id, get_all_my_favorite_sql, get_all_templates_with_category_id
from tgbot.utils.misc_functions import get_all_fonts


#### ОТОБРАЖЕНИЕ СТРАН ПРИ СОЗДАНИИ КАТЕГОРИИ #####
async def select_all_countries_to_add_cat_kb(remover):
    get_categories = get_all_countries()
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['country_name'],
                                 callback_data=f"add_new_category_in_select_country:{get_categories[a]['country_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"add_new_category_in_select_country_swipe:{remover + 5}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"add_new_category_in_select_country_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"add_new_category_in_select_country_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"add_new_category_in_select_country_swipe:{remover + 5}"),
            )
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))

        return keyboard
    else:
        return None

#### ОТОБРАЖЕНИЕ СТРАН ПРИ СОЗДАНИИ ШАБЛОНА #####
async def select_all_countries_to_add_template_kb(remover):
    get_categories = get_all_countries()
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['country_name'],
                                 callback_data=f"add_new_template_in_select_country:{get_categories[a]['country_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"add_new_template_in_select_country_swipe:{remover + 5}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"add_new_template_in_select_country_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"add_new_template_in_select_country_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"add_new_template_in_select_country_swipe:{remover + 5}"),
            )
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))

        return keyboard
    else:
        return None


#### ОТОБРАЖЕНИЕ КАТЕГОРИЙ ПРИ СОЗДАНИИ ШАБЛОНА #####
async def select_all_categories_to_add_template_kb(remover, country_id):
    get_categories = get_all_categories_with_country_id(country_id)
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                 callback_data=f"add_new_template_in_select_category:{get_categories[a]['country_id']}:{get_categories[a]['category_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"add_new_template_in_select_category_swipe:{remover + 5}:{country_id}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"add_new_template_in_select_category_swipe:{remover - 5}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"add_new_template_in_select_category_swipe:{remover - 5}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"add_new_template_in_select_category_swipe:{remover + 5}:{country_id}"),
            )
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))

        return keyboard
    else:
        return None


# ОТОБРАЖЕНИЕ СТРАН ПРИ ОТРИСОВКЕ ПО ГОТОВОМУ ШАБЛООНУ
async def select_all_countries_to_make_drawing_kb(remover):
    try:
        get_categories = get_all_countries()
    except Exception as e:
        print(e)
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['country_name'],
                                 callback_data=f"select_country_in_drawing:{get_categories[a]['country_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"select_country_in_drawing_swipe:{remover + 5}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"select_country_in_drawing_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"select_country_in_drawing_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"select_country_in_drawing_swipe:{remover + 5}"),
            )
        keyboard.add(InlineKeyboardButton(text='☑️ Скрыть', callback_data='hide_msg'))
        return keyboard
    else:
        return None


# ОТОБРАЖЕНИЕ КАТЕГОРИЙ ПРИ ОТРИСОВКЕ ПО ГОТОВОМУ ШАБЛООНУ
async def select_all_categories_to_make_drawing_kb(remover, country_id):
    get_categories = get_all_categories_with_country_id(country_id)
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                 callback_data=f"show_all_templates_to_drawing:{get_categories[a]['country_id']}:{get_categories[a]['category_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"show_all_templates_to_drawing_swipe:{remover + 5}:{country_id}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"show_all_templates_to_drawing_swipe:{remover - 5}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"show_all_templates_to_drawing_swipe:{remover - 5}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"show_all_templates_to_drawing_swipe:{remover + 5}:{country_id}"),
            )
        return keyboard
    else:
        return None


# ОТОБРАЖЕНИЕ ШАБЛОНОВ ПРИ ОТРИСОВКЕ ПО ГОТОВОМУ ШАБЛООНУ
async def select_all_templates_to_make_drawing_kb(remover, category_id, country_id):
    get_categories = get_all_templates_with_category_id(category_id)
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['template_name'],
                                 callback_data=f"use_template:{get_categories[a]['template_id']}:{get_categories[a]['file_name']}:{country_id}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"show_templates_swipe:{remover + 5}:{category_id}:{country_id}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"show_templates_swipe:{remover - 5}:{category_id}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"show_templates_swipe:{remover - 5}:{category_id}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"show_templates_swipe:{remover + 5}:{category_id}:{country_id}"),
            )
        keyboard.add(InlineKeyboardButton(text='◀️ Назад', callback_data=f'select_country_in_drawing:{country_id}'))

        return keyboard
    else:
        return None

# ОТОБРАЖЕНИЕ ВСЕХ ШРИФТОВ
async def font_keyboard(remover,layer_id):
    get_categories = get_all_fonts()
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['font_name'],
                                 callback_data=f"show_all_fonts_use_font:{get_categories[a]['font_name']}:{layer_id}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"show_all_fonts_swipe:{remover + 5}:{layer_id}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"show_all_fonts_swipe:{remover - 5}:{layer_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"show_all_fonts_swipe:{remover - 5}:{layer_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"show_all_fonts_swipe:{remover + 5}:{layer_id}"),
            )
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))
        return keyboard
    else:
        return None

# ПОЛУЧЕНИЕ ИЗБРАННОГО
async def select_all_my_favorite(remover, user_id):
    get_categories = get_all_my_favorite_sql(user_id)
    if get_categories:
        keyboard = InlineKeyboardMarkup()
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['template_name'],
                                 callback_data=f"use_template:{get_categories[a]['template_id']}:{get_categories[a]['file_name']}:{get_categories[a]['country_id']}:{True}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"favorite_swipe:{remover + 5}:{user_id}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"favorite_swipe:{remover - 5}:{user_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"favorite_swipe:{remover - 5}:{user_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"favorite_swipe:{remover + 5}:{user_id}"),
            )
        keyboard.add(InlineKeyboardButton(text='☑️ Скрыть', callback_data='hide_msg'))
        return keyboard
    else:
        return None


#### ОТОБРАЖЕНИЕ СТРАН ПРИ СОЗДАНИИ ШАБЛОНА ПОЛЬЗОВАТЕЛЕМ #####
async def select_all_countries_to_create_template_kb(remover):
    get_categories = get_all_countries()
    keyboard = InlineKeyboardMarkup()
    if get_categories:
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['country_name'],
                                 callback_data=f"create_template_in_exist_country:{get_categories[a]['country_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"create_template_in_exist_country_swipe:{remover + 5}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"create_template_in_exist_country_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"create_template_in_exist_country_swipe:{remover - 5}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"create_template_in_exist_country_swipe:{remover + 5}"),
            )
        keyboard.add(InlineKeyboardButton(text='🏁 Создать страну', callback_data='create_new_user_country'))
        keyboard.add(InlineKeyboardButton(text='☑️ Скрыть', callback_data='hide_msg'))

        return keyboard
    else:
        keyboard.add(InlineKeyboardButton(text='🏁 Создать страну', callback_data='create_new_user_country'))
        keyboard.add(InlineKeyboardButton(text='☑️ Скрыть', callback_data='hide_msg'))
        return keyboard


#### ОТОБРАЖЕНИЕ КАТЕГОРИЙ ПРИ СОЗДАНИИ ШАБЛОНА #####
async def select_all_categories_to_create_template_kb(remover, country_id):
    get_categories = get_all_categories_with_country_id(country_id)
    keyboard = InlineKeyboardMarkup()
    if get_categories:
        if remover >= len(get_categories): remover -= 5
        for count, a in enumerate(range(remover, len(get_categories))):
            if count < 5:
                keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                 callback_data=f"add_new_template_in_select_category:{get_categories[a]['country_id']}:{get_categories[a]['category_id']}"))

        if len(get_categories) <= 5:
            pass
        elif len(get_categories) > 5 and remover < 5:
            keyboard.add(
                InlineKeyboardButton(f"1/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"create_template_in_exist_category_swipe:{remover + 5}:{country_id}"),
            )
        elif remover + 5 >= len(get_categories):
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"create_template_in_exist_category_swipe:{remover - 5}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
            )
        else:
            keyboard.add(
                InlineKeyboardButton("⬅️", callback_data=f"create_template_in_exist_category_swipe:{remover - 5}:{country_id}"),
                InlineKeyboardButton(f"{str(int((remover + 5)/5))}/{math.ceil(len(get_categories) / 5)}", callback_data="..."),
                InlineKeyboardButton("➡️", callback_data=f"create_template_in_exist_category_swipe:{remover + 5}:{country_id}"),
            )
        keyboard.add(InlineKeyboardButton(text='🗂 Создать категорию', callback_data=f'create_new_user_category:{country_id}'))
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))

        return keyboard
    else:
        keyboard.add(InlineKeyboardButton(text='🗂 Создать категорию', callback_data=f'create_new_user_category:{country_id}'))
        keyboard.add(InlineKeyboardButton(text='❌ Отменить', callback_data='hide_msg'))
        return keyboard