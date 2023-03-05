# - *- coding: utf- 8 - *-
import sqlite3
import aiosqlite

from tgbot.utils.const_functions import get_unix
from tgbot.data.config import PATH_DATABASE


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE active = 1 AND "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя
def add_userx(user_id, username,time):
    try:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            con.execute("INSERT INTO users "
                        "(id, status, username, date) "
                        "VALUES (?, ?, ?, ?)",
                        [user_id, 0, username, time])
            con.commit()
    except Exception as e:
        print(e)


# Получения переменных для профиля
def get_info_for_profile_menu(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = f"SELECT count(*) FROM likes WHERE user_id = {user_id}"
        likes = con.execute(sql).fetchone()
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = f"SELECT count(*) FROM templates WHERE creator_id = {user_id}"
        templates = con.execute(sql).fetchone()
    return likes[0], templates[0]


# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получения слоя
def get_templatex(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM templates"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение слоя
def get_layerx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM template_layers"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        return con.execute(sql).fetchall()


# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()


def update_layerx(layer_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE template_layers SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(layer_id)
        con.execute(sql + "WHERE layer_id = ?", parameters)
        con.commit()

# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Добавление новой страны
async def sql_add_new_country(country_name, active=1):
    if active == 1:
        async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("INSERT INTO template_countries (country_name) VALUES (?)", (country_name,))
            await db.commit()
    else:
        async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("INSERT INTO template_countries (country_name, active) VALUES (?, ?)", (country_name, 0))
            await db.commit()

# Добавление новой категории
async def sql_add_new_category(category_name, country_id, active=1):
    if active == 1:
        async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("INSERT INTO template_categories (category_name, country_id) VALUES (?, ?)", (category_name, country_id,))
            await db.commit()
    else:
        async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("INSERT INTO template_categories (category_name, country_id, active) VALUES (?, ?, ?)", (category_name, country_id,0,))
            await db.commit()

# Добавление нового шаблона
async def sql_add_new_template(category_id, country_id, creator_id, file_name, template_name, description, active = 1):
    if active == 1:
        async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("INSERT INTO templates (category_id, country_id, creator_id, file_name, template_name, description) VALUES (?, ?, ?, ?, ?, ?)", (category_id, country_id, creator_id, file_name, template_name, description,))
            await db.commit()
    else:
        async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("INSERT INTO templates (category_id, country_id, creator_id, file_name, template_name, description, active) VALUES (?, ?, ?, ?, ?, ?, ?)", (category_id, country_id, creator_id, file_name, template_name, description, 0))
            await db.commit()

# Получение всех страх
def get_all_countries(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM template_countries WHERE active = 1"
        return con.execute(sql).fetchall()

# Получение country_name
def get_country_name_with_country_id(country_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = "SELECT country_name FROM template_countries WHERE country_id = {}".format(country_id)
        return con.execute(sql).fetchone()

# Получение всех категорий с ID конкретной страны
def get_all_categories_with_country_id(country_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM template_categories WHERE country_id = {} AND active = 1".format(country_id)
        return con.execute(sql).fetchall()

# Получение template_id по имени
def get_template_with_file_name(file_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM templates WHERE file_name = {}".format(file_name)
        return (con.execute(sql).fetchone())

# Удаление шаблона
async def delete_template_with_template_id(template_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("DELETE FROM templates WHERE template_id = ?", (template_id,))
        await db.execute("DELETE FROM template_layers WHERE template_id = ?", (template_id,))
        await db.commit()

# Получение характеристик слоя
async def get_all_from_layer(template_id, layer_name):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM template_layers WHERE template_id = ? AND layer_name = ? AND active = 1', (template_id, layer_name)) as cursor:
            layer_info = await cursor.fetchone()
            return layer_info

# Добавление нового слоя
async def sql_add_new_layer(template_id, layer_name):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("INSERT INTO template_layers (template_id, layer_name) VALUES (?, ?)", (template_id, layer_name))
        await db.commit()

# Обновление выравнивания по центру
async def update_layer_align_center(layer_id, old_align):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        if old_align == 1:
            await db.execute("UPDATE template_layers SET align_center = 0 where layer_id = (?)", (layer_id,))
        if old_align == 0:
            await db.execute("UPDATE template_layers SET align_center = 1 where layer_id = (?)", (layer_id,))
            await db.execute("UPDATE template_layers SET align_right = 0 where layer_id = (?)", (layer_id,))
        await db.commit()

# Обновление выравнивания по центру
async def update_layer_align_right(layer_id, old_align):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        if old_align == 1:
            await db.execute("UPDATE template_layers SET align_right = 0 where layer_id = (?)", (layer_id,))
        if old_align == 0:
            await db.execute("UPDATE template_layers SET align_center = 0 where layer_id = (?)", (layer_id,))
            await db.execute("UPDATE template_layers SET align_right = 1 where layer_id = (?)", (layer_id,))
        await db.commit()

# Получение характеристик слоя
async def get_all_from_layer_with_layer_id(layer_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM template_layers WHERE layer_id = ? AND active = 1', (layer_id,)) as cursor:
            layer_info = await cursor.fetchone()
            return layer_info

# Получение category_id
async def get_user_category(country_id, category_name):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM template_categories WHERE country_id = ? AND category_name = ?', (country_id,category_name,)) as cursor:
            category_info = await cursor.fetchone()
            return category_info

# Получение country_id
async def get_user_country(country_name):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM template_countries WHERE country_name = ?', (country_name,)) as cursor:
            layer_info = await cursor.fetchone()
            return layer_info

# Получение всех слоев
def get_all_layers(template_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM template_layers WHERE template_id = {template_id} AND active = 1"
        return con.execute(sql).fetchall()

def get_all_templates_with_category_id(category_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM templates WHERE category_id = {category_id} AND active = 1"
        return con.execute(sql).fetchall()

# Получение названия файла
async def get_file_name_with_template_id(template_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT file_name FROM templates WHERE template_id = ?', (template_id,)) as cursor:
            template_name = await cursor.fetchone()
            return template_name

# Удаление слоя
async def delete_layer(layer_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("DELETE FROM template_layers WHERE layer_id = ?", (layer_id,))
        await db.commit()

# Получение лайков
async def is_like_template(user_id, template_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT user_id FROM likes WHERE user_id = ? AND template_id = ?', (user_id,template_id,)) as cursor:
            is_like = await cursor.fetchone()
            return is_like

# Добавление лайка
async def add_like(template_id, user_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("INSERT INTO likes (user_id, template_id) VALUES (?, ?)", (user_id, template_id))
        await db.commit()

# Удаление лайка
async def delete_like(template_id, user_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("DELETE FROM likes WHERE user_id = ? AND template_id = ?", (user_id, template_id))
        await db.commit()

# Получение всех лайков
def get_all_likes(template_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = f"SELECT COUNT(*) FROM likes WHERE template_id = {template_id}"
        return (con.execute(sql).fetchone())[0]

# Получение избранного
async def is_favorite_func(template_id, user_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT user_id FROM favorite WHERE user_id = ? AND template_id = ?', (user_id,template_id,)) as cursor:
            is_like = await cursor.fetchone()
            return is_like

# Добавление в избранное
async def add_favorite(template_id, user_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("INSERT INTO favorite (user_id, template_id) VALUES (?, ?)", (user_id, template_id))
        await db.commit()

# Удаление из избранного
async def del_favorite(template_id, user_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute("DELETE FROM favorite WHERE user_id = ? AND template_id = ?", (user_id, template_id))
        await db.commit()

# Получение всего избранного  для динамической клавиатуры
def get_all_my_favorite_sql(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"select favorite.template_id, templates.template_name, templates.file_name, templates.country_id FROM favorite JOIN templates ON favorite.template_id=templates.template_id WHERE favorite.user_id = {user_id}"
        return con.execute(sql).fetchall()


# Получение информации о шаблоне созданным пользователем
async def get_all_from_user_template(template_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM templates WHERE template_id = ?', (template_id,)) as cursor:
            template_info = await cursor.fetchone()
            return template_info

# Получение информации о стране созданным пользователем
async def get_all_from_user_country(country_id):
    print(country_id)
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM template_countries WHERE country_id = ?', (country_id,)) as cursor:
            template_info = await cursor.fetchone()
            return template_info

# Получение информации о категории созданной пользователем
async def get_all_from_user_category(category_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
        async with db.execute('SELECT * FROM template_categories WHERE category_id = ?', (category_id,)) as cursor:
            template_info = await cursor.fetchone()
            return template_info


# Одобрение шаблона
async def accept_template(template_id, country_id, category_id):
    async with aiosqlite.connect(PATH_DATABASE) as db:
            await db.execute("UPDATE templates SET active = 1 where template_id = (?)", (template_id,))
            await db.execute("UPDATE template_countries SET active = 1 where country_id = (?)", (country_id,))
            await db.execute("UPDATE template_categories SET active = 1 where category_id = (?)", (category_id,))
            await db.commit()