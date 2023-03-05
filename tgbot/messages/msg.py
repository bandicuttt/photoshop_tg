from tgbot.services.api_sqlite import get_info_for_profile_menu, get_template_with_file_name, get_userx


def sub_message(message):
    return(
f'''
<b>
– Для использования нашего бота вы должны быть подписаны на наш канал, спасибо за понимание!😘♥️
</b>
'''
    )

def template_admin_check_message(message):
    return(
f'''
<b>
– Ваш шаблон отправлен на модерацию!👮🏻‍♂️

<i>Если Ваш шаблон пройдёт модерацию, то им смогут воспользоваться и другие люди.</i>

– Средний срок проверки каждого шаблона в течении 24х часов с момента отправки.
</b>
'''
    )

def format_html_message():
    return(
f'''
<b>Жирный</b>
<i>Курсив</i>
<u>Подчеркнутый</u>
<code>Моно</code>
<s>Зачеркнутый</s>
<a href='здесь ссылка'>Тест ссылки</a>
'''
    )

def is_still_sub_message(message):
    return(
f'''
<b>– Вы отписались от нашего канала, без этого вы не сможете использовать бот 😰</b>
'''
    )

def captcha_message(message, count):
    return(
f'''
<b>
– Проверка на робота👮🏻‍♂️

<i>С целью адекватной работы нашего проекта, мы должны убедиться в том, что вы живой человек. 

Для продолжение введите число с картинки выше.</i>

– К-ство попыток: {count}
</b>
'''
    )

def start_message(message):
    return(
f'''<b><i>
Приветствую, @{message.from_user.username} 🖖🏻

Этот инновационный проект дает возможность каждому использовать бесплатные шаблоны различных сервисов и создавать их самому.
</i></b>
'''
    )

def second_main_message():
    return(
f'''<b><i>
Совершая любые действия в проекте, Вы подтверждаете своё согласие с правилами сообщества. 

Приятного Вам использования♥️
</i></b>
'''
    )

def profile_message(message):
    user_info = get_userx(id=message.from_user.id)
    like_count, template_count = get_info_for_profile_menu(message.from_user.id)
    date = user_info['date'][0:10].replace('-','.')
    yy = date.split('.')[0]
    mm = date.split('.')[1]
    dd = date.split('.')[2]
    return(
f'''
<b>– Профиль👨🏻‍💻</b>

<b>Дата:</b> {dd}.{mm}.{yy}г
<b>ID:</b> {message.from_user.id}
<b>Шаблоны:</b> {template_count} 
<b>Лайки:</b> {like_count}

<b>– Будем благодарны за находку любой недоработки в проекте🥰</b>
'''
    )


def admin_menu_message(message):
    return(
f'''
<b>– Панель администратора 👨🏻‍🔧</b>

<i>Здесь вы управлять вашим ботом.</i>
'''
    )


def layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right):
    data = {1: 'Да', 0: 'Нет'}
    return(
f'''
<b>👩‍🎨 Создание слоя </b>

<b>Название:</b> <code>{layer_name}</code>
<b>Шрифт:</b> <code>{font}</code>
<b>Цвет:</b> <code>{font_color}</code>
<b>Координаты:</b> <code>{coordinates}</code>
<b>Выровнять по центру:</b> <code>{data.get(align_center)}</code>
<b>Выровнять по правой стороне:</b> <code>{data.get(align_right)}</code>

<b>👇  Выберите действие</b>
'''
    )


def use_template(message, template_info):
    return(
f'''
<b>🏷 Название:</b> <code>{template_info['template_name']}</code>
<b>💭 Описание:</b> <code>{template_info['description']}</code>
'''
        )


def check_template_admin_menu(message,template_info, country_info, category_info):
    try:
        print(template_info)
        print(country_info)
        print(category_info)
        data = {0: 'NEW ❗️', 1: ''}
        country_name = str(country_info[1] + ' ' + data.get(country_info[2]))
        category_name = str(category_info[1] + ' ' + data.get(category_info[3]))


        
        return(
    f'''
<b>⚠️ ШАБЛОН НА МОДЕРАЦИИ ⚠️</b>
<b>🆔 Создатель шаблона: {template_info[3]}</b>
<b>🏁 Страна: {country_name}</b>
<b>🗂 Категория: {category_name}</b>
<b>💭 Описание: {template_info[6]}</b>
<b>🏷 Название шаблона: {template_info[5]}</b>
    '''
        )
    except Exception as e:
        print(e)
        print('ошибка здесь')