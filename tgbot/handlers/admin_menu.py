# - *- coding: utf- 8 - *-
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes
from random import randint
import os

from tgbot.data.config import get_admins
from tgbot.data.loader import dp
from tgbot.utils.misc.bot_filters import IsAdmin
from tgbot.messages.msg import admin_menu_message, check_template_admin_menu, layer_edit_message, profile_message
from tgbot.keyboards.inline_admin import accept_spam, accept_spam_keyboard, add_file_to_spam, admin_menu_keyboard
from tgbot.keyboards.inline_all import check_template_admin, hide_message_keyboard, edit_my_tempalte_keyboard, edit_layer_keyboard, main_keyboard_menu
from tgbot.services.api_sqlite import accept_template, delete_layer, delete_template_with_template_id, get_all_from_layer_with_layer_id, get_all_from_user_category, get_all_from_user_country, get_all_from_user_template, get_all_layers, get_all_usersx, sql_add_new_country, sql_add_new_category, sql_add_new_template, get_template_with_file_name, get_all_from_layer, sql_add_new_layer, update_layer_align_right, update_layer_align_center
from tgbot.keyboards.dynamic_inline_all  import select_all_countries_to_add_cat_kb, select_all_countries_to_add_template_kb, select_all_categories_to_add_template_kb, select_all_countries_to_create_template_kb, select_all_countries_to_make_drawing_kb, select_all_my_favorite
from tgbot.utils.misc_functions import create_qr_code, is_font, prescreen_func


@dp.message_handler(state='blank', text=['👨🏻‍🔧 Панель администратора','🎨 Шаблоны','👨‍🎨 Создать', '✨ Избранное','👨‍💻 Профиль'])
async def return_and_delete(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        msg = message.text
        if msg == '👨🏻‍🔧 Панель администратора':
            try:
                await state.finish()
                await message.delete()

                proxy['msg']=await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text=admin_menu_message(message),
                    reply_markup=admin_menu_keyboard()
                )
                await state.set_state('blank')
            except Exception as e:
                print(e)
        if msg == '🎨 Шаблоны':
            try:
                await state.finish()
                await message.delete()
                keyboard = await select_all_countries_to_make_drawing_kb(0)
                if keyboard:
                    proxy['msg']=await message.bot.send_message(
                        chat_id=message.from_user.id,
                        text='<b>– Выберите страну шаблона✍🏻</b>',
                        reply_markup=keyboard
                    )
                    await state.set_state('blank')
                else:
                    await message.answer('😔 | Страны не найдены.', reply_markup=hide_message_keyboard('Hide_this'))
            except Exception as e:
                print(e)
        if msg == '👨‍🎨 Создать':
            async with state.proxy() as proxy:
                await state.finish()
                await message.delete()

                keyboard = await select_all_countries_to_create_template_kb(0)
                proxy['msg']=await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text='<b>– Выберите страну или создайте новую🧑🏻‍🎨</b>',
                    reply_markup=keyboard,
                )
                await state.set_state('blank')
        if msg == '✨ Избранное':
            async with state.proxy() as proxy:
                try:
                    await state.finish()
                    await message.delete()
                    keyboard = await select_all_my_favorite(0, message.from_user.id)
                    if keyboard:
                        proxy['msg']=await message.bot.send_message(
                            chat_id=message.from_user.id,
                            text='<b>– Список ваших избранных шаблонов✨</b>',
                            reply_markup=keyboard
                        )
                        await state.set_state('blank')
                    else:
                        await message.answer('<b>– Избранные шаблоны не найдены✨</b>',reply_markup=hide_message_keyboard('Hide_this'))
                except Exception as e:
                    print(e)
        if msg == '👨‍💻 Профиль':
            async with state.proxy() as proxy:
                try:
                    await state.finish()
                    await message.delete()

                    proxy['msg']=await message.bot.send_message(
                        message.from_user.id,
                        text=profile_message(message),
                        reply_markup=main_keyboard_menu(message.from_user.id),
                    )
                    await state.set_state('blank')
                except Exception as e:
                    print(e)



####################### ОБРАБОТЧИК АДМИНКИ ################
@dp.message_handler(IsAdmin(),text='👨🏻‍🔧 Панель администратора', state='*')
async def admin_menu_fdasfsadf(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        try:
            await state.finish()
            await message.delete()

            proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                text=admin_menu_message(message),
                reply_markup=admin_menu_keyboard()
            )
            await state.set_state('blank')
        except Exception as e:
            print(e)

@dp.callback_query_handler(text='spam', state='*')
async def spam_admin_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['msg'] = await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>✍️ | Введите сообщение для рассылки</b>\n\nВы можете использовать HTML разметку для оформления текста!',
            reply_markup=hide_message_keyboard('Cancel')
        )
        await state.set_state('get_message_for_spam')

@dp.message_handler(state='get_message_for_spam')
async def precheck_spam(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        try: 
                await message.delete()
                proxy['text'] = message.text
                proxy['msg']=await message.bot.edit_message_text(
                    chat_id=message.from_user.id,
                    reply_markup=accept_spam_keyboard(),
                    message_id=proxy['msg'].message_id,
                    text='<b>📣 Проверка</b>\n{}\n<i>Вы точно хотите использовать это сообщение ? Подтвердите или отправьте новое сообщение.</i>'.format(message.text)
                )
        except Exception as e:
            print(e)
            print(message.text)
            proxy['msg'] = await message.bot.send_message(
                chat_id=message.from_user.id,
                text='❌ Вы допустили ошибку используя теги. Попробуйте ещё раз!',
                reply_markup=hide_message_keyboard('Cancel'),
            )

@dp.callback_query_handler(state='get_message_for_spam', text='get_file')
async def accept_text(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['msg']=await call.bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.from_user.id,
            text='<b>✍️ | Желаете добавить файл ?</b>',
            reply_markup=add_file_to_spam()
        )

@dp.callback_query_handler(state='get_message_for_spam', text_startswith='add_file')
async def get_file(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        try:
            mode = call.data.split(':')[1]
            if mode == 'True':
                proxy['msg']=await call.bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text='<b>✍️ | Отправьте желаемый файл</b>',
                reply_markup=hide_message_keyboard('Cancel')
                )
            else:
                proxy['msg']=await call.bot.edit_message_text(
                    chat_id=call.from_user.id,
                    reply_markup=accept_spam(),
                    message_id=proxy['msg'].message_id,
                    text='<b>📣 Проверка</b>\n{}\n<i>Вы точно хотите разослать это сообщение пользователям ?</i>'.format(proxy['text'])
                )
                proxy['file_path'] = None
                proxy['file_type'] = 'text'
            await state.set_state('get_file_for_spam')
        except Exception as e:
            print(e)



@dp.message_handler(state='get_file_for_spam', content_types=ContentTypes.ANY)
async def add_new_template(message: Message, state: FSMContext):
    try:
        async with state.proxy() as proxy:

            await proxy['msg'].delete()
            await message.delete()

            if message.document:
                file_id = message.document.file_id
                proxy['file_type'] = 'document'

            elif message.video:
                file_id = message.video.file_id
                proxy['file_type'] = 'video'

            elif message.animation:
                file_id = message.animation.file_id
                proxy['file_type'] = 'animation'
            
            elif message.photo:
                file_id = message.photo[-1].file_id
                proxy['file_type'] = 'photo'
            else:
                return await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text='<b>❌ Ошибка! Скорее всего вы отправили файл, который не поддерживается.</b>'
                )
            
            file = await message.bot.get_file(file_id)
            file_path = file.file_path
            file_type = str(file['file_path']).split('.')[1]

            while True:
                file_name = randint(0, 99999999)
                if os.path.exists('tgbot/files/temp/{}.{}'.format(file_name,file_type)):
                    pass
                else:
                    await message.bot.download_file(file_path, 'tgbot/files/temp/{}.{}'.format(file_name,file_type))
                    break

            file_path = f'tgbot/files/temp/{file_name}.{file_type}'
            proxy['file_path'] = file_path
            caption = proxy['text']
            caption = f'<b>📣 Проверка:</b>\n{caption}\n\n<b>Вы точно хотите использовать это сообщение ? Подтвердите или отправьте новый файл.</b>'
            with open(file_path,'rb') as document:
                if message.video:
                    proxy['msg']=await message.bot.send_video(
                        chat_id=message.from_user.id,
                        caption=caption,
                         reply_markup=accept_spam(),
                        video=document,
                    )
                if message.animation:
                    proxy['msg']=await message.bot.send_animation(
                        chat_id=message.from_user.id,
                        caption=caption,
                         reply_markup=accept_spam(),
                        animation=document
                    )
                if message.photo:
                    proxy['msg']=await message.bot.send_photo(
                        chat_id=message.from_user.id,
                        caption=caption,
                         reply_markup=accept_spam(),
                        photo=document
                    )
                if message.document:
                    proxy['msg']=await message.bot.send_document(
                        chat_id=message.from_user.id,
                        caption=caption,
                        reply_markup=accept_spam(),
                        document=document
                    )
    except Exception as e:
        print(e)

@dp.callback_query_handler(state='get_file_for_spam', text='accept_spam')
async def spam_func(call: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            bad = 0
            good = 0
            text = proxy['text']
            file_path = proxy['file_path']
            file_type = proxy['file_type']

            msg=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>🕔 Рассылка началась...</b>'
            )
            for user in get_all_usersx():
                try:
                    if 'text' not in file_type:
                        with open(file_path,'rb') as document:
                            if file_type == 'photo':
                                await call.bot.send_photo(
                                    chat_id=user['id'],
                                    reply_markup=hide_message_keyboard('Hide_this'),
                                    caption=text,
                                    photo=document
                                )
                            if file_type == 'document':
                                await call.bot.send_document(
                                    chat_id=user['id'],
                                    reply_markup=hide_message_keyboard('Hide_this'),
                                    caption=text,
                                    document=document
                                )
                            if file_type == 'animation':
                                await call.bot.send_animation(
                                    chat_id=user['id'],
                                    reply_markup=hide_message_keyboard('Hide_this'),
                                    caption=text,
                                    animation=document
                                )
                            if file_type == 'video':
                                await call.bot.send_video(
                                    chat_id=user['id'],
                                    reply_markup=hide_message_keyboard('Hide_this'),
                                    caption=text,
                                    video=document
                                )
                    if file_type == 'text':
                        await call.bot.send_message(
                            chat_id=user['id'],
                            reply_markup=hide_message_keyboard('Hide_this'),
                            text=text,
                        )
                    await asyncio.sleep(0.1)
                    good+=1
                except Exception as e:
                    print(e)
                    bad+=1
            os.remove(file_path)
            await state.finish()
            await call.bot.edit_message_text(
                message_id=msg.message_id,
                chat_id=call.from_user.id,
                text='<b>✅ | Рассылка завершена</b>\n\n<b>💌 Пользователей получило рассылку: {}</b>\n<b>😔 Пользователей заблокировало бота: {}</b>'.format(good, bad),
                reply_markup=hide_message_keyboard('Hide')
            )
    except  Exception as e:
        print(e)


@dp.callback_query_handler(text='add_new_font', state='*')
async def add_new_font(call: CallbackQuery, state: FSMContext):
    await call.bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=hide_message_keyboard('Cancel'),
        text='✍️ | Отправьте новый шрифт файлом'
    )
    await state.set_state('add_new_font')

@dp.message_handler(state='add_new_font', content_types=['document'])
async def get_font_from_user(message: Message, state: FSMContext):
    try:
        file_name = message.document.file_name
        if is_font(message.document.file_name):
            file_id = message.document.file_id
            file = await message.bot.get_file(file_id)
            file_path = file.file_path
            await message.bot.download_file(file_path, 'tgbot/files/fonts/{}'.format(file_name))
            await message.bot.send_message(
                text='<b>🎉 | Шрифт успешно загружен</b>',
                reply_markup=hide_message_keyboard('Hide'),
                chat_id=message.from_user.id)
            await state.finish()
        else:
            await message.bot.send_message(
                text='<b>❌ | Шрифт с таким именем существует. Попробуйте ещё раз или отмените.</b>',
                reply_markup=hide_message_keyboard('Cancel'),
                chat_id=message.from_user.id)
    except Exception as e:
        print(e)
    

####################### СОЗДАНИЕ НОВОЙ СТРАНЫ ###########################
@dp.callback_query_handler(IsAdmin(), text='add_new_country', state='*')
async def add_new_country_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await state.finish()

        proxy['msg'] = await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>✍️ | Введите название новой страны</b>',
            reply_markup=hide_message_keyboard()
        )
        await state.set_state('add_new_country:set_country_name')

@dp.message_handler(IsAdmin(), state='add_new_country:set_country_name')
async def add_new_country(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()

        await state.finish()

        await sql_add_new_country(message.text)

        await message.bot.send_message(
            chat_id=message.from_user.id,
            text='<b>🎉 | Добавлена новая страна</b>',
            reply_markup=hide_message_keyboard('Hide')
        )


##################### СОЗДАНИЕ НОВОЙ КАТЕГОРИИ ##########################
@dp.callback_query_handler(IsAdmin(), text='add_new_category', state='*')
async def add_new_category_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:

        keyboard = await select_all_countries_to_add_cat_kb(0)
        if keyboard:
            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | В какую страну добавить категорию?</b>',
                reply_markup=keyboard,
            )
            await state.set_state('temp_state_1')
            
        else:
            await call.answer('😔 | Страны не найдены. Сначала добавьте страну', show_alert=False)

@dp.callback_query_handler(text_startswith='add_new_category_in_select_country_swipe:', state='*')
async def country_swiper(call: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            await proxy['msg'].delete()

            proxy['msg']=await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text='<b>✍️ | В какую страну добавить категорию?</b>',
                    reply_markup=await select_all_countries_to_add_cat_kb(int(call.data.split(':')[1])),
                )
    except Exception as e:
        print(e)

@dp.callback_query_handler(text_startswith='add_new_category_in_select_country:', state='*')
async def add_new_category_in_select_country_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await call.message.delete()

        country_id = call.data.split(':')[1]
        proxy['country_id'] = country_id
        proxy['msg']=await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>✍️ | Введите название категории</b>',
            reply_markup=hide_message_keyboard('Cancel')
        )
            
        await state.set_state('add_new_category:select_name')

@dp.message_handler(state='add_new_category:select_name')
async def add_new_category(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await state.finish()
        await proxy['msg'].delete()
        await message.delete()

        await sql_add_new_category(message.text, proxy['country_id'])
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text='<b>🎉 | Новая категория успешно создана!</b>',
            reply_markup=hide_message_keyboard('Hide')
        )

##################### СОЗДАНИЕ НОВОГО ШАБЛОНА ##########################
@dp.callback_query_handler(text='add_new_template', state='*')
async def add_new_template_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await state.finish()
        keyboard = await select_all_countries_to_add_template_kb(0)
        if keyboard:
            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | Выберите в какой стране создать шаблон</b>',
                reply_markup=keyboard
            )
            await state.set_state('temp_state')
        else:
            await call.answer('😔 | Страны не найдены. Сначала добавьте страну', show_alert=False)

@dp.callback_query_handler(text_startswith='add_new_template_in_select_country_swipe:', state='*')
async def add_new_template_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()

        proxy['msg'] = await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>✍️ | Выберите в какой стране создать шаблон</b>',
            reply_markup=await select_all_countries_to_add_template_kb(int(call.data.split(':')[1]))
        )

@dp.callback_query_handler(text_startswith='add_new_template_in_select_country:', state='*')
async def add_new_template_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:

        keyboard = await select_all_categories_to_add_template_kb(0, call.data.split(':')[1])
        if keyboard:
            await proxy['msg'].delete()
            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | Выберите в какой категории создать шаблон</b>',
                reply_markup=keyboard
            )
        else:
            await call.answer('😔 | Категории не найдены. Сначала добавьте категорию', show_alert=False)

@dp.callback_query_handler(text_startswith='add_new_template_in_select_category_swipe:', state='*')
async def add_new_template_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()

        remover = int(call.data.split(':')[1])
        country_id = call.data.split(':')[2]
        proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | Выберите в какой категории создать шаблон</b>',
                reply_markup=await select_all_categories_to_add_template_kb(remover, country_id)
            )


@dp.callback_query_handler(text_startswith='add_new_template_in_select_category:', state='*')
async def add_new_template_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await call.message.delete()
        await state.finish()
        
        proxy['country_id'] = call.data.split(':')[1]
        proxy['category_id'] = call.data.split(':')[2]

        proxy['msg']=await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Введите название для создания шаблона 🧑🏻‍🎨</b>',
            reply_markup=hide_message_keyboard(text='Cancel')
        )
        await state.set_state('add_new_template:set_name')

@dp.message_handler(state='add_new_template:set_name')
async def add_new_template_func(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()

        proxy['template_name'] = message.text
        proxy['msg']=await message.bot.send_message(
            chat_id=message.from_user.id,
            text='<b>– Введите описание для создания Вашего шаблона 🧑🏻‍🎨</b>',
            reply_markup=hide_message_keyboard(text='Cancel')
        )
        await state.set_state('add_new_template:set_description')

@dp.message_handler(state='add_new_template:set_description')
async def add_new_template_func(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()

        proxy['template_description'] = message.text
        proxy['msg']=await message.bot.send_message(
            chat_id=message.from_user.id,
            text='<b>– Отправьте фотографию для создания шаблона 🧑🏻‍🎨\n\n<i>UPD: Без сжатия, файлом ⚠️</i></b>',
            reply_markup=hide_message_keyboard(text='Cancel')
        )
        await state.set_state('add_new_template:set_photo')


@dp.message_handler(state='add_new_template:set_photo', content_types=['document'])
async def add_new_template(message: Message, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            await proxy['msg'].delete()
            await message.delete()

            category_id = proxy['category_id']
            country_id = proxy['country_id']
            creator_id = message.from_user.id
            template_name = proxy['template_name']
            description = proxy['template_description']

            while True:
                file_name = randint(0, 99999999)
                if os.path.exists('tgbot/files/image source/{}.jpg'.format(file_name)):
                    pass
                else:
                    proxy['file_name'] = file_name
                    file_id = message.document.file_id
                    file = await message.bot.get_file(file_id)
                    file_path = file.file_path
                    await message.bot.download_file(file_path, 'tgbot/files/image source/{}.jpg'.format(file_name))
                    break
            if message.from_user.id in get_admins():
                await sql_add_new_template(category_id, country_id, creator_id, file_name, template_name, description)
            else:
                await sql_add_new_template(category_id, country_id, creator_id, file_name, template_name, description, 0)
            
            template_id = get_template_with_file_name(file_name)['template_id']
            await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>– Меню создание шаблона 🧑🏻‍🎨\n\n<i>Выберите действия👇🏻</i></b>',
                reply_markup=edit_my_tempalte_keyboard(template_id, True)
            )
    except Exception as e:
        print(e)

# @dp.message_handler(state='add_new_template:set_photo', content_types=['photo'])
# async def add_new_template(message: Message, state: FSMContext):
#     try:
#         async with state.proxy() as proxy:
#             await proxy['msg'].delete()
#             await message.delete()

#             category_id = proxy['category_id']
#             country_id = proxy['country_id']
#             creator_id = message.from_user.id
#             template_name = proxy['template_name']
#             description = proxy['template_description']

#             while True:
#                 file_name = randint(0, 99999999)
#                 if os.path.exists('tgbot/files/image source/{}.jpg'.format(file_name)):
#                     pass
#                 else:
#                     proxy['file_name'] = file_name
#                     await message.photo[-1].download(destination_file='tgbot/files/image source/{}.jpg'.format(file_name))
#                     break
#             await sql_add_new_template(category_id, country_id, creator_id, file_name, template_name, description)
            
#             template_id = get_template_with_file_name(file_name)['template_id']
#             print(template_id)
#             await message.bot.send_message(
#                 chat_id=message.from_user.id,
#                 text='<b>♦️ | Меню редактирования шаблона </b>',
#                 reply_markup=edit_my_tempalte_keyboard(template_id, False)
#             )
#     except Exception as e:
#         print(e)

##################### РАБОТА СО СЛОЯМИ ##########################
@dp.callback_query_handler(text_startswith='delete_template:', state='*')
async def delete_template(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    template_id = call.data.split(':')[1]

    await delete_template_with_template_id(template_id)

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>✅ | Создание шаблона успешно отменено </b>',
        reply_markup=hide_message_keyboard('Hide')
    )

@dp.callback_query_handler(text_startswith='add_new_layer:', state='*')
async def add_new_layer(call: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            proxy['template_id'] = call.data.split(':')[1]
            await call.message.delete()
            if len(call.data.split(':')) < 3:
                proxy['msg']=await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text='<b>– Введите название слоя 🧑🏻‍🎨</b>\n\n<i>Именно этот текст будет отображаться на фотографии.</i>',
                    reply_markup=hide_message_keyboard('Cancel')
                )
                await state.set_state('add_new_layer:set_layer_name')
            else:
                proxy['msg']=await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text='<b>– Введите ссылку для QR кода 🧑🏻‍🎨</b>\n\n<i>Формат: https://google.com</i>',
                    reply_markup=hide_message_keyboard('Cancel')
                )
                await state.set_state('add_new_layer:set_qr_code')
    except Exception as e:
        print(e)


@dp.message_handler(state='add_new_layer:set_qr_code')
async def set_qr_code(message: Message, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            await proxy['msg'].delete()
            await message.delete()

            template_id = proxy['template_id']

            while True:
                file_name = randint(0, 99999999)
                if os.path.exists('tgbot/files/image cache/{}_{}.png'.format(message.text,file_name)):
                    pass
                else:
                    layer_name = await create_qr_code(message.text, file_name)
                    break
            
            layer_name = str(message.text) + ':' + str(file_name)
            await sql_add_new_layer(template_id, layer_name)
            layer_info = await get_all_from_layer(template_id, layer_name)

            layer_id = layer_info[0]
            font = layer_info[3]
            font_color = layer_info[8]
            font_size = layer_info[4]
            coordinates = layer_info[5]
            align_center = layer_info[6]
            align_right = layer_info[7]

            await message.bot.send_message(
                chat_id=message.from_user.id,
                text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right,font_size,qr=True),
                reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right,qr=True)
            )
    except Exception as e:
        print(e)


@dp.message_handler(state='add_new_layer:set_layer_name')
async def set_layer_name(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()

        template_id = proxy['template_id']
        layer_name = message.text

        await sql_add_new_layer(template_id, layer_name)
        layer_info = await get_all_from_layer(template_id, layer_name)

        layer_id = layer_info[0]
        font = layer_info[3]
        font_color = layer_info[8]
        coordinates = layer_info[5]
        align_center = layer_info[6]
        align_right = layer_info[7]
        font_size = layer_info[4]
        if 'https' in layer_name or 'http' in layer_name:
            qr = True
        else:
            qr = None

        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right, font_size,qr),
            reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right, qr)
        )


@dp.callback_query_handler(text_startswith='change_layer_align:', state='*')
async def change_layer_align(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = {1: 0, 0: 1}

    mode = call.data.split(':')[1]
    layer_id = call.data.split(':')[3]
    template_id = call.data.split(':')[2]
    layer_info = await get_all_from_layer_with_layer_id(layer_id)
    font = layer_info[3]
    font_color = layer_info[8]
    coordinates = layer_info[5]
    layer_name = layer_info[2]
    font_size = layer_info[4]

    if mode == 'center':
        old_align = layer_info[6]
        await update_layer_align_center(layer_id, old_align)

    if mode == 'right':
        old_align = layer_info[7]
        await update_layer_align_right(layer_id, old_align)
    
    layer_info = await get_all_from_layer_with_layer_id(layer_id)
    new_align_center = layer_info[6]
    new_align_right = layer_info[7]
    if 'https' in layer_name or 'http' in layer_name:
        qr = True
    else:
        qr = None

    await call.bot.send_message(
            chat_id=call.from_user.id,
            text=layer_edit_message(layer_name, font, font_color, coordinates, new_align_center, new_align_right, font_size,qr),
            reply_markup=edit_layer_keyboard(layer_id, template_id, new_align_center, new_align_right,qr)
        )

@dp.callback_query_handler(text_startswith='prescreem_with_layers:', state='*')
async def prescreen_with_layers(call: CallbackQuery, state: FSMContext):
    # await call.message.delete()
    
    tempalte_id = call.data.split(':')[1]
    # layer_id = call.data.split(':')[2]

    image = await prescreen_func(tempalte_id)
    with image as document:
        await call.bot.send_document(
            chat_id=call.from_user.id,
            caption='<b>– В настоящее время ваш шаблон выглядит так 🧑🏻‍🎨</b>',
            reply_markup=hide_message_keyboard('Hide_this'),
            document=document
        )
    # await call.bot.send_photo(
    #     chat_id=call.from_user.id,
    #     photo = image,
    #     caption='<b>👩‍🎨 | На данный момент ваш шаблон выглядит так:</b>',
    #     reply_markup=hide_message_keyboard('Hide_this')
    # )

@dp.callback_query_handler(text_startswith='delete_layer:', state='*')
async def delete_layer_func(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    layer_id = call.data.split(':')[2]
    template_id = call.data.split(':')[1]

    await delete_layer(layer_id)
    layers_info = get_all_layers(template_id)
    
    
    if len(layers_info):
        await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>– Меню создание шаблона 🧑🏻‍🎨\n\n<i>Выберите действия👇🏻</i></b>',
                reply_markup=edit_my_tempalte_keyboard(template_id, True)
            )
    else:
        await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>– Меню создание шаблона 🧑🏻‍🎨\n\n<i>Выберите действия👇🏻</i></b>',
                reply_markup=edit_my_tempalte_keyboard(template_id, True)
            )

@dp.callback_query_handler(text_startswith='layer_is_ready:', state='*')
async def ready_layer(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    template_id = call.data.split(':')[1]

    await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Меню создание шаблона 🧑🏻‍🎨\n\n<i>Выберите действия👇🏻</i></b>',
            reply_markup=edit_my_tempalte_keyboard(template_id, True, 0)
        )

@dp.callback_query_handler(text_startswith='next_layers:', state='*')
async def layers_swiper(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    template_id = call.data.split(':')[2]
    remover = int(call.data.split(':')[1])

    await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Меню создание шаблона 🧑🏻‍🎨\n\n<i>Выберите действия👇🏻</i></b>',
            reply_markup=edit_my_tempalte_keyboard(template_id, True, remover)
        )

@dp.callback_query_handler(text_startswith='template_ready:', state='*')
async def template_ready(call: CallbackQuery, state: FSMContext):
    try:
        await state.finish()
        await call.message.delete()
        template_id = call.data.split(':')[1]
        img = await prescreen_func(template_id)
        admin_list = get_admins()
        if call.from_user.id in admin_list:
            await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✅ | Шаблон успешно сохранен!</b>',
                reply_markup=hide_message_keyboard('Hide')
            )
        else:
            template_info = await get_all_from_user_template(template_id)
            country_info = await get_all_from_user_country(template_info[2])
            category_info = await get_all_from_user_category(template_info[1])
            await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>🎉 | Ваш шаблон отправлен на модерацию!</b>\n<i>Если ваш шаблон пройдёт модерацию, то им смогут воспользоваться и другие люди!</i>',
                reply_markup=hide_message_keyboard('Hide')
            )
            await call.bot.send_photo(
                chat_id=admin_list[0],
                photo=img,
                caption=check_template_admin_menu(call, template_info, country_info, category_info),
                reply_markup=check_template_admin(template_id)
            )
    except Exception as e:
        print(e)


@dp.callback_query_handler(text_startswith='show_layers:', state='*')
async def show_layer_menu_to_edit_smth(call: CallbackQuery, state: FSMContext):
    layer_id = call.data.split(':')[1]
    template_id = call.data.split(':')[2]

    await call.message.delete()

    layer_info = await get_all_from_layer_with_layer_id(layer_id)

    layer_name = layer_info[2]
    layer_id = layer_info[0]
    font = layer_info[3]
    font_color = layer_info[8]
    coordinates = layer_info[5]
    align_center = layer_info[6]
    align_right = layer_info[7]
    font_size = layer_info[4]
    if 'https' in layer_name or 'http' in layer_name:
        qr = True
    else:
        qr = None

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right, font_size,qr),
        reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right,qr)
    )

@dp.callback_query_handler(text_startswith='accept_template_admin:')
async def accept_user_template(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    template_id = call.data.split(':')[1]
    template_info = await get_all_from_user_template(template_id)
    country_info = await get_all_from_user_country(template_info[2])
    category_info = await get_all_from_user_category(template_info[1])

    country_id = country_info[0]
    category_id = category_info[0]

    await accept_template(template_id, country_id, category_id)

    await call.bot.send_message(
        chat_id=template_info[3],
        text='<b>🎉 | Ваш шаблон одобрен, поздравляем !</b>',
        reply_markup=hide_message_keyboard('Hide')
    )
