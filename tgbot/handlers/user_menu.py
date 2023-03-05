# - *- coding: utf- 8 - *-
import os
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from tgbot.data.config import get_admins

from aiogram.dispatcher.handler import CancelHandler
from tgbot.data.loader import dp
from tgbot.keyboards.dynamic_inline_all import font_keyboard, select_all_categories_to_create_template_kb, select_all_categories_to_make_drawing_kb, select_all_countries_to_create_template_kb, select_all_countries_to_make_drawing_kb, select_all_my_favorite, select_all_templates_to_make_drawing_kb
from tgbot.messages.msg import layer_edit_message, profile_message, use_template
from tgbot.messages.msg import start_message
from tgbot.keyboards.inline_all import create_user_template_custom, edit_coordinates_pre_screen_kb, edit_layer_keyboard, edit_my_tempalte_keyboard, hide_message_keyboard, main_keyboard_menu, use_template_menu
from tgbot.services.api_sqlite import add_favorite, add_like, del_favorite, delete_like, get_all_layers, get_country_name_with_country_id, get_layerx, get_template_with_file_name, get_templatex, get_user_category, get_user_country, is_favorite_func, is_like_template, sql_add_new_category, sql_add_new_country, update_layerx
from tgbot.utils.misc_functions import edit_coordinates_pre_check_func, prescreen_user_func


######################################################################
###################### ОБРАБОТЧИКИ СТОРОННИХ КНОПОК ##################
@dp.callback_query_handler(text='back_to_main_menu', state='*')
async def back_to_main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=open('tgbot/files/bot_image/main_img.jpg','rb'),
        caption=start_message(call),
        reply_markup=main_keyboard_menu(call.from_user.id)
    )


@dp.callback_query_handler(text='hide_msg', state='*')
async def back_to_main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

######################################################################
###################### ОБРАБОТЧИКИ КНОПОК ГЛАВНОГО МЕНЮ ##############
@dp.message_handler(text='👨‍💻 Профиль', state='*')
async def view_profile(message: Message, state: FSMContext):
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
        except CancelHandler():
            pass
        except Exception as e:
            print(e)

######################################################################
###################### ОТРИСОВКА #####################################
@dp.message_handler(text='🎨 Шаблоны', state='*')
async def create_drawing_choosing_country(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        try:
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

@dp.callback_query_handler(text_startswith='select_country_in_drawing_swipe:', state='*')
async def country_swiper(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    remover = int(call.data.split(':')[1])
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>– Выберите страну шаблона✍🏻</b>',
        reply_markup=await select_all_countries_to_make_drawing_kb(remover)
    )

@dp.callback_query_handler(text_startswith='select_country_in_drawing:', state='*')
async def create_drawing_choosing_category_in_country(call: CallbackQuery, state: FSMContext):
    country_id = call.data.split(':')[1]
    print(country_id)
    keyboard = await select_all_categories_to_make_drawing_kb(0, country_id)
    if keyboard:
        await call.message.delete()
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Выберите категорию шаблона для редактирования✍🏻</b>',
            reply_markup=keyboard
        )
        await state.finish()
    else:
        await call.answer('😔 | Категории в этой стране не найдены.', show_alert=False)

@dp.callback_query_handler(text_startswith='edit_my_template:')
async def edit_my_template(call: CallbackQuery, state: FSMContext):
    try:
        template_id = call.data.split(':')[1]
        await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text='<b>– Меню создание шаблона 🧑🏻‍🎨\n\n<i>Выберите действия👇🏻</i></b>',
                    reply_markup=edit_my_tempalte_keyboard(template_id, True)
                )
    except Exception as e:
        print(e)

@dp.callback_query_handler(text_startswith='show_all_templates_to_drawing_swipe:',state='*')
async def category_swiper(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    country_id = call.data.split(':')[2]
    remover = int(call.data.split(':')[1])

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>✍️ | Выберите категорию отрисовки </b>',
        reply_markup=await select_all_categories_to_make_drawing_kb(remover, country_id)
    )


@dp.callback_query_handler(text_startswith='show_all_templates_to_drawing:',state='*')
async def show_all_templates_in_category(call: CallbackQuery, state: FSMContext):
    conutry_id = call.data.split(':')[1]
    category_id = call.data.split(':')[2]
    keyboard = await select_all_templates_to_make_drawing_kb(0,category_id, conutry_id)
    if keyboard:
        await call.message.delete()
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>✍️ | Выберите шаблон отрисовки </b>',
            reply_markup=keyboard
        )
    else:
        await call.answer('😔 | Шаблоны в этой категории не найдены.', show_alert=False)


@dp.callback_query_handler(text_startswith='show_templates_swipe:',state='*')
async def templates_swiper(call: CallbackQuery, state: FSMContext):
    conutry_id = call.data.split(':')[3]
    category_id = call.data.split(':')[2]
    remover = int(call.data.split(':')[1])
    keyboard = await select_all_templates_to_make_drawing_kb(remover,category_id, conutry_id)
    if keyboard:
        await call.message.delete()
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>✍️ | Выберите шаблон отрисовки </b>',
            reply_markup=keyboard
        )
    else:
        await call.answer('😔 | Шаблоны в этой категории не найдены.', show_alert=False)


@dp.callback_query_handler(text_startswith='use_template:', state='*')
async def use_template_func(call: CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        if len(call.data.split(':')) == 5:
            profile = True
        else:
            profile = False
        template_id = call.data.split(':')[1]
        file_name = call.data.split(':')[2]
        template_info = get_template_with_file_name(file_name)
        await call.message.delete()

        if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
            image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
        else:
            image = open(f'tgbot/files/image source/{file_name}.jpg','rb')

        # with image as document:
        #     await call.bot.send_document(
        #         chat_id=call.from_user.id,
        #         document=document,
        #         caption=use_template(call, template_info),
        #         reply_markup=use_template_menu(template_id, template_info['country_id'], template_info['category_id'], template_info['file_name'], profile=profile),
        #     )

        await call.bot.send_photo(
            chat_id=call.from_user.id,
            photo=image,
            caption=use_template(call, template_info),
            reply_markup=use_template_menu(template_id, template_info['country_id'], template_info['category_id'], template_info['file_name'], call.from_user.id),
        )
    except Exception as e:
        print('ошибка блять')
        print(e)

@dp.callback_query_handler(text_startswith='user_use_template:', state='*')
async def use_template_func(call: CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        async with state.proxy() as proxy:
            # await call.message.delete()

            template_id = call.data.split(':')[1]
            file_name = call.data.split(':')[2]

            if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
                image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
            else:
                image = open(f'tgbot/files/image source/{file_name}.jpg','rb')
            layers = get_all_layers(template_id)
            layers_list = []
            for i in layers:
                layer_name = i['layer_name']
                if 'https' in layer_name:
                    layer_name = i['layer_name'].split(':')[0] + ':' + i['layer_name'].split(':')[1]
                layers_list.append(f'<b>♦️ {layer_name}</b>')
            layers_list = '\n'.join(layers_list)
            message = f'<b>👩‍🎨 Введите аргументы: </b>\n\n{layers_list}'

            with image as document:
                proxy['msg'] = await call.bot.send_document(
                    chat_id = call.from_user.id,
                    document=document,
                    caption=message,
                    reply_markup=hide_message_keyboard('Cancel'),
                )

            # proxy['msg'] = await call.bot.send_photo(
            #     chat_id = call.from_user.id,
            #     photo=image,
            #     caption=message,
            #     reply_markup=hide_message_keyboard('Cancel'),
            # )
            proxy['layers'] = layers
            proxy['caption'] = message
            proxy['file_name'] = file_name
            proxy['template_id'] = template_id

            await state.set_state('await_arugments_to_draw')
    except Exception as e:
        print(e)


@dp.message_handler(state='await_arugments_to_draw')
async def draw_my_template(message: Message, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            layers = proxy['layers']
            caption = proxy['caption']
            file_name = proxy['file_name']
            template_id = proxy['template_id']
            if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
                image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
            else:
                image = open(f'tgbot/files/image source/{file_name}.jpg','rb')


            if len((message.text).split('\n')) == len(layers):
                await message.delete()
                await proxy['msg'].delete()
                layers_name = message.text.split('\n')
                image = await prescreen_user_func(template_id, file_name, layers_name)
                with image as document:
                    await message.bot.send_document(
                        message.from_user.id,
                        document=document,
                        caption='<b>👩‍🎨 Ваш шаблон готов! </b>',
                        reply_markup=hide_message_keyboard('Hide'),
                    )
                # await message.bot.send_photo(
                #     chat_id=message.from_user.id,
                #     caption='<b>👩‍🎨 Ваш шаблон готов! </b>',
                #     reply_markup=hide_message_keyboard('Hide'),
                #     photo=image
                # )
                await state.finish()
            else:
                caption = caption + '\n\n➖➖➖➖➖➖➖➖➖➖➖➖\n<b>❌ Введено неверное количество аргументов!\nПопробуйте ещё раз!</b>'
                await message.delete()
                await proxy['msg'].delete()
                with image as document:
                    proxy['msg']=await message.bot.send_document(
                        chat_id=message.from_user.id,
                        document=image,
                        caption=caption,
                        reply_markup=hide_message_keyboard('Cancel'),
                    )
                # proxy['msg']=await message.bot.send_photo(
                #     chat_id=message.from_user.id,
                #     caption=caption,
                #     photo=image,
                #     reply_markup=hide_message_keyboard('Cancel'),
                # )
    except Exception as e:
        print(e)


@dp.callback_query_handler(text_startswith='edit_layer:', state='*')
async def edit_layer(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        mode = call.data.split(':')[1]
        proxy['layer_id'] = call.data.split(':')[2]
        layer_id = proxy['layer_id']
        if mode == 'name':
            await state.finish()

            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>– Введите название слоя 🧑🏻‍🎨</b>\n\n<i>Этот текст будет отображаться в шаблоне.</i>',
                reply_markup=hide_message_keyboard('Cancel')
            )
            await state.set_state('edit_name')

        if mode == 'font_size':
            await state.finish()

            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | Отправьте новый размер шрифта</b>',
                reply_markup=hide_message_keyboard('Cancel')
            )
            await state.set_state('edit_font_size')
        
        if mode == 'font':
            await state.finish()

            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>– Выберите нужный шрифт для создания шаблона 🧑🏻‍🎨</b>',
                reply_markup=await font_keyboard(0, layer_id),
            )
        if mode == 'color':
            await state.finish()

            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>– Выберите цвет шрифта 🧑🏻‍🎨</b>\n\n<i>Формат HEX: #000000 ⚠️</i>',
                reply_markup=hide_message_keyboard('Cancel')
            )
            await state.set_state('edit_font_color')
        
        if mode == 'coordinates':
            await state.finish()

            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>– Введите координаты слоя 🧑🏻‍🎨</b>\n\n<i>Формат: 100,100 ⚠️</i>',
                reply_markup=hide_message_keyboard('Cancel')
            )
            await state.set_state('edit_coordinates')

@dp.message_handler(state='edit_coordinates')
async def edit_coordinates(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await message.delete()
        layer_id = proxy['layer_id']
        try:
            coordinates = (message.text.replace(' ','')).split(',')
            if int(coordinates[0]) and int(coordinates[1]) > 0:
                await proxy['msg'].delete()
                layer_info = get_layerx(layer_id=layer_id)
                template_id = layer_info['template_id']
                image = await edit_coordinates_pre_check_func(template_id, coordinates)
                await message.bot.send_document(
                    chat_id=message.from_user.id,
                    document=image,
                    caption='<b>👩‍🎨 Использовать эти координаты?</b>\n',
                    reply_markup=edit_coordinates_pre_screen_kb(layer_id, coordinates[0], coordinates[1])
                )
                await state.set_state('set_coordinates_ready')
            else:
                await proxy['msg'].delete()
                proxy['msg']=await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text='<b>– Введите координаты слоя 🧑🏻‍🎨</b>\n\n<i>Неверно, введите ещё раз ⚠️</i>',
                    reply_markup=hide_message_keyboard('Cancel')
                    )
        except Exception as e:
            print(e)
            await proxy['msg'].delete()
            proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>– Введите координаты слоя 🧑🏻‍🎨</b>\n\n<i>Неверно, введите ещё раз ⚠️</i>',
                reply_markup=hide_message_keyboard('Cancel')
                )

@dp.callback_query_handler(state='set_coordinates_ready', text_startswith='set_coordinates:')
async def set_my_coordinates(call: CallbackQuery, state: FSMContext):
    try:
        layer_id = call.data.split(':')[1]
        width = call.data.split(':')[2]
        height = call.data.split(':')[3]
        coordinates = str(f'{width},{height}')
        await call.message.delete()
        await state.finish()
        update_layerx(layer_id, coordinates=coordinates)
        layer_info = get_layerx(layer_id=layer_id)
        layer_name = layer_info['layer_name']
        if 'https' in layer_name or 'http' in layer_name:
            qr = True
        else:
            qr = None
        font = layer_info['font']
        font_color = layer_info['font_color']
        align_center = layer_info['align_center']
        align_right = layer_info['align_right']
        template_id = layer_info['template_id']
        font_size = layer_info['font_size']

        await call.bot.send_message(
            chat_id=call.from_user.id,
            text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right,font_size,qr),
            reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right,qr)
        )
        # await call.bot.send_message(
        #         chat_id=call.from_user.id,
        #         text='<b>🎉 | Координаты слоя успешно изменены!</b>',
        #         reply_markup=hide_message_keyboard('Hide')
        #     )
    except Exception as e:
        print(e)

@dp.message_handler(state='edit_font_color')
async def edit_font_color(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()

        layer_id = proxy['layer_id']
        if '#' in message.text and len(message.text) < 15:
            update_layerx(layer_id, font_color=message.text)
            layer_info = get_layerx(layer_id=layer_id)
            layer_name = layer_info['layer_name']
            font = layer_info['font']
            font_color =layer_info['font_color']
            coordinates = layer_info['coordinates']
            align_center = layer_info['align_center']
            align_right = layer_info['align_right']
            template_id = layer_info['template_id']
            font_size = layer_info['font_size']
            if 'https' in layer_name or 'http' in layer_name:
                qr = True
            else:
                qr = None

            await message.bot.send_message(
                chat_id=message.from_user.id,
                text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right, font_size,qr),
                reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right,qr)
            )
            # await message.bot.send_message(
            #     chat_id=message.from_user.id,
            #     text='<b>🎉 | Цвет шрифта успеншо изменен!</b>',
            #     reply_markup=hide_message_keyboard('Hide')
            # )
            await state.finish()
        else:
            proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>– Введите цвет слоя 🧑🏻‍🎨</b>\n\n<i>Неверно, введите ещё раз ⚠️</i>',
                reply_markup=hide_message_keyboard('Cancel')
            )



@dp.message_handler(state='edit_name')
async def layer_edit_name(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()
        layer_id = proxy['layer_id']
        update_layerx(layer_id, layer_name=message.text)
        layer_info = get_layerx(layer_id=layer_id)
        layer_name = layer_info['layer_name']
        font = layer_info['font']
        font_color =layer_info['font_color']
        coordinates = layer_info['coordinates']
        align_center = layer_info['align_center']
        align_right = layer_info['align_right']
        template_id = layer_info['template_id']
        font_size = layer_info['font_size']
        if 'https' in layer_name or 'http' in layer_name:
            qr = True
        else:
            qr = None

        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right, font_size,qr),
            reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right,qr)
        )
        # await message.bot.send_message(
        #     chat_id=message.from_user.id,
        #     text='<b>🎉 | Название слоя успешно изменено!</b>',
        #     reply_markup=hide_message_keyboard('Hide')
        # )
        await state.finish()

@dp.message_handler(state='edit_font_size')
async def layer_edit_font_size(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()
        try:
            if float(message.text) > 0:
                layer_id = proxy['layer_id']
                update_layerx(layer_id, font_size=message.text)
                layer_info = get_layerx(layer_id=layer_id)
                layer_name = layer_info['layer_name']
                font = layer_info['font']
                font_color =layer_info['font_color']
                coordinates = layer_info['coordinates']
                align_center = layer_info['align_center']
                align_right = layer_info['align_right']
                template_id = layer_info['template_id']
                font_size = layer_info['font_size']
                if 'https' in layer_name or 'http' in layer_name:
                    qr = True
                else:
                    qr = None

                await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right,font_size, qr),
                    reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right, qr)
                )
                # await message.bot.send_message(
                #     chat_id=message.from_user.id,
                #     text='<b>🎉 | Размер шрифта успешно изменен!</b>',
                #     reply_markup=hide_message_keyboard('Hide')
                # )
                await state.finish()
            else:
                proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>– Введите размер шрифта 🧑🏻‍🎨</b>\n\n<i>Неверно, введите ещё раз ⚠️</i>',
                reply_markup=hide_message_keyboard('Cancel')
            )
        except Exception as e:
            proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>– Введите размер шрифта 🧑🏻‍🎨</b>\n\n<i>Неверно, введите ещё раз ⚠️</i>',
                reply_markup=hide_message_keyboard('Cancel')
            )


@dp.callback_query_handler(text_startswith='show_all_fonts_swipe:', state='*')
async def font_swiper(call: CallbackQuery, state: FSMContext):
    remover = call.data.split(':')[1]
    layer_id = call.data.split(':')[2]
    await call.message.delete()
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>✍️ | Выберите нужный шрифт</b>',
        reply_markup=await font_keyboard(int(remover), layer_id),
    )

@dp.callback_query_handler(text_startswith='show_all_fonts_use_font', state='*')
async def change_font(call: CallbackQuery, state: FSMContext):
    layer_id = call.data.split(':')[2]
    font_name = (call.data.split(':')[1]).split('.')[0]
    update_layerx(layer_id, font=font_name)
    await call.message.delete()
    layer_info = get_layerx(layer_id=layer_id)
    layer_name = layer_info['layer_name']
    font = layer_info['font']
    font_color =layer_info['font_color']
    coordinates = layer_info['coordinates']
    align_center = layer_info['align_center']
    align_right = layer_info['align_right']
    template_id = layer_info['template_id']
    font_size = layer_info['font_size']
    if 'https' in layer_name or 'http' in layer_name:
        qr = True
    else:
        qr = None

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=layer_edit_message(layer_name, font, font_color, coordinates, align_center, align_right,font_size, qr),
        reply_markup=edit_layer_keyboard(layer_id, template_id, align_center, align_right, qr)
    )
    # await call.bot.send_message(
    #     chat_id=call.from_user.id,
    #     text='<b>🎉 | Шрифт успешно изменен!</b>',
    #     reply_markup=hide_message_keyboard('Hide')
    # )
@dp.callback_query_handler(text_startswith='like_this_template:', state='*')
async def use_template_func(call: CallbackQuery, state: FSMContext):
    template_id = call.data.split(':')[1]
    country_id = call.data.split(':')[2]
    category_id = call.data.split(':')[3] 
    file_name = call.data.split(':')[4]
    is_like = await is_like_template(call.from_user.id, template_id)
    if is_like:
        await delete_like(template_id, call.from_user.id)
        await call.answer('🎉 | Вы убрали лайк шаблону', show_alert=False)
    else:
        await add_like(template_id, call.from_user.id)
        await call.answer('🎉 | Вы поставили лайк шаблону', show_alert=False)
    template_info = get_template_with_file_name(file_name)

    if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
        image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
    else:
        image = open(f'tgbot/files/image source/{file_name}.jpg','rb')

    with image as document:
        await call.bot.send_document(
            chat_id=call.from_user.id,
            document=document,
            caption=use_template(call, template_info),
            reply_markup=use_template_menu(template_id, country_id, category_id, file_name, call.from_user.id),
        )
    await call.message.delete()


@dp.callback_query_handler(text_startswith='add_to_favorite:', state='*')
async def add_to_favorite(call: CallbackQuery, state: FSMContext):
    template_id = call.data.split(':')[1]
    country_id = call.data.split(':')[2]
    category_id = call.data.split(':')[3] 
    file_name = call.data.split(':')[4]
    user_id = call.from_user.id

    is_favorite = await is_favorite_func(template_id, user_id)
    if is_favorite:
        await del_favorite(template_id, user_id)
        await call.answer('🎉 | Вы удалили шаблон из избранного', show_alert=False)
        fav=True
    else:
        await add_favorite(template_id, user_id)
        await call.answer('🎉 | Вы добавили шаблон в избранное', show_alert=False)
        fav=None

    template_info = get_template_with_file_name(file_name)

    if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
        image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
    else:
        image = open(f'tgbot/files/image source/{file_name}.jpg','rb')

    with image as document:
        await call.bot.send_document(
            chat_id=call.from_user.id,
            document=document,
            caption=use_template(call, template_info),
            reply_markup=use_template_menu(template_id, country_id, category_id, file_name, call.from_user.id, fav ),
        )
    await call.message.delete()



@dp.message_handler(text='✨ Избранное', state='*')
async def get_my_favorite(message: Message, state: FSMContext):
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


@dp.callback_query_handler(text_startswith='favorite_swipe', state='*')
async def fav_swiper(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Список ваших избранных шаблонов✨</b>',
            reply_markup=await select_all_my_favorite(int(call.data.split(':')[1]), call.from_user.id)
        )
    except Exception as e:
        print(e)

@dp.message_handler(text='👨‍🎨 Создать', state='*')
async def create_my_template(message: Message, state: FSMContext):
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

@dp.callback_query_handler(text_startswith='create_template_in_exist_country_swipe', state='*')
async def country_swiper_in_create_country_user(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    remover = int(call.data.split(':')[1])
    keyboard = await select_all_countries_to_create_template_kb(remover)
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>– Выберите страну или создайте новую🧑🏻‍🎨</b>',
        reply_markup=keyboard,
    )


@dp.callback_query_handler(text_startswith='create_template_in_exist_country:', state='*')
async def create_user_template_in_exist_country(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    country_id = call.data.split(':')[1]
    keyboard = await select_all_categories_to_create_template_kb(0, country_id)
    
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>– Выберите категорию или создайте новую🧑🏻‍🎨</b>',
        reply_markup=keyboard
    )




@dp.callback_query_handler(text_startswith='create_template_in_exist_category_swipe:', state='*')
async def category_swiper_in_create_category_user(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    remover = int(call.data.split(':')[1])
    country_id = call.data.split(':')[2]
    keyboard = await select_all_categories_to_create_template_kb(remover, country_id)
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text='<b>– Выберите категорию или создайте новую🧑🏻‍🎨</b>',
        reply_markup=keyboard
    )


@dp.callback_query_handler(text='create_new_user_country', state='*')
async def create_new_user_country(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await state.finish()

        proxy['msg']=await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Введите название новой страны 🧑🏻‍🎨</b>',
            reply_markup=hide_message_keyboard('Cancel')
        )

        await state.set_state('create_user_country')

@dp.message_handler(state='create_user_country')
async def get_new_country_name(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        try:
            if message.from_user.id in get_admins():
                await sql_add_new_country(message.text, 1)
            else:
                await sql_add_new_country(message.text, 0)
            await message.delete()
            await proxy['msg'].delete()
            country_info = await get_user_country(message.text)
            print(country_info)
            proxy['country_id'] = country_info[0]
            proxy['country_name'] = message.text

            proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>– Введите название новой категории 🧑🏻‍🎨</b>',
                reply_markup=hide_message_keyboard('Cancel')
            )

            await state.set_state('create_user_category_in_new_country')
        except Exception as e:
            print(e)

@dp.message_handler(state='create_user_category_in_new_country')
async def create_new_category_in_new_country(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()

        country_id = proxy['country_id']
        if message.from_user.id in get_admins():
            await sql_add_new_category(message.text, country_id, 1)
        else:
            await sql_add_new_category(message.text, country_id, 0)
        category_info = await get_user_category(country_id, message.text)
        category_id = category_info[0]
        country_name = proxy['country_name']

        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=f'<b>Страна и категория созданы успешно🧑🏻‍🎨</b>\n\n<b>🏴Страна: {country_name}</b>\n<b>🗂️Категория: {message.text}</b>\n\n<i>Проверьте введенные данные, если они верны, то нажмите снизу кнопку «Продолжить».</i>',
            reply_markup=create_user_template_custom(country_id, category_id)
        )
        await state.finish()


@dp.callback_query_handler(text_startswith='create_new_user_category:', state='*')
async def create_new_user_category_in_exist_country(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    async with state.proxy() as proxy:
        country_id = call.data.split(':')[1]
        proxy['country_id'] = country_id
        proxy['country_name'] = (get_country_name_with_country_id(country_id))[0]

        proxy['msg']=await call.bot.send_message(
            chat_id=call.from_user.id,
            text='<b>– Введите название новой категории 🧑🏻‍🎨</b>',
            reply_markup=hide_message_keyboard('Cancel')
        )

        await state.set_state('create_user_category_in_new_country')




