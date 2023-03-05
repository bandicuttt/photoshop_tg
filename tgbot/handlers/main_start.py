# - *- coding: utf- 8 - *-
import os
import random
from captcha.image import ImageCaptcha

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.keyboards.inline_all import hide_message_keyboard, main_keyboard_menu, use_template_menu
from tgbot.data.loader import dp
from tgbot.keyboards.reply_all import main_menu_reply
from tgbot.services.api_sqlite import get_template_with_file_name, get_userx, update_userx
from tgbot.messages.msg import captcha_message, second_main_message, start_message, use_template
from tgbot.utils.misc.bot_filters import IsSubMessage


image = ImageCaptcha(width = 280, height = 90)
captcha_attempt = 3

@dp.message_handler(IsSubMessage(),text=('/start'), state="*")
async def main_start(message: Message, state: FSMContext):
    try:
        await state.finish()

        user_id = message.from_user.id
        user_info = get_userx(id=user_id)
        if user_info['captcha'] == 1:
            await message.bot.send_photo(
                chat_id=message.from_user.id,
                photo=open('tgbot/files/bot_image/main_img.jpg','rb'),
                caption=start_message(message),
                reply_markup=main_menu_reply(message.from_user.id)
            )
            await message.bot.send_message(
                chat_id=message.from_user.id,
                reply_markup=main_keyboard_menu(),
                text=second_main_message(),
            )
        else:
            async with state.proxy() as proxy:
                captcha_text = str(random.randint(1000, 50000))
                proxy['captcha'] = captcha_text
                proxy['attempt'] = 1
                
                proxy['msg']=await message.bot.send_photo(
                    message.from_user.id,
                        image.generate(captcha_text),
                        caption=captcha_message(message, 3)
                        )
                await state.set_state('captcha')
    except Exception as e:
        print(e)


@dp.callback_query_handler(IsSubMessage(),text=('check_me'), state="*")
async def main_start(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    try:
        await state.finish()

        user_id = call.from_user.id
        user_info = get_userx(id=user_id)
        if user_info['captcha'] == 1:
            await call.bot.send_photo(
                chat_id=call.from_user.id,
                photo=open('tgbot/files/bot_image/main_img.jpg','rb'),
                caption=start_message(call),
                reply_markup=main_menu_reply(call.from_user.id)
            )
            await call.bot.send_message(
                chat_id=call.from_user.id,
                reply_markup=main_keyboard_menu(),
                text=second_main_message(),
            )
        else:
            async with state.proxy() as proxy:
                captcha_text = str(random.randint(1000, 50000))
                proxy['captcha'] = captcha_text
                proxy['attempt'] = 1
                
                proxy['msg']=await call.bot.send_photo(
                    call.from_user.id,
                        image.generate(captcha_text),
                        caption=captcha_message(call, 3)
                        )
                await state.set_state('captcha')
    except Exception as e:
        print(e)

### ОБРАБОТЧИК ЕСЛИ ССЫЛКА ЧТО-ТО СОДЕРЖИТ
@dp.message_handler(IsSubMessage(),text_startswith='/start ')
async def referal_template(message: Message, state: FSMContext):
    image = ImageCaptcha(width = 280, height = 90)
    try:
        await state.finish()

        user_id = message.from_user.id
        user_info = get_userx(id=user_id)
        if user_info['captcha'] == 1:
            temp = message.text.split(' ')[1]
            template_id = temp.split('_')[0]
            file_name = temp.split('_')[1]
            country_id = temp.split('_')[2]
            template_info = get_template_with_file_name(file_name)
            await message.delete()

            if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
                image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
            else:
                image = open(f'tgbot/files/image source/{file_name}.jpg','rb')

            with image as document:
                msg=await message.bot.send_message(
                chat_id=message.from_user.id,
                reply_markup=main_menu_reply(message.from_user.id),
                text='<i>Приятного пользования</i>'
                )
                await message.bot.send_document(
                    chat_id=message.from_user.id,
                    document=document,
                    caption=use_template(message, template_info),
                    reply_markup=use_template_menu(template_id, template_info['country_id'], template_info['category_id'], template_info['file_name'], profile=True),
                ) 

        else:
            async with state.proxy() as proxy:
                captcha_text = str(random.randint(1000, 50000))
                proxy['captcha'] = captcha_text
                proxy['attempt'] = 1
                proxy['referal_link'] = message.text
                proxy['msg']=await message.bot.send_photo(
                    message.from_user.id,
                    image.generate(captcha_text),
                    caption=captcha_message(message, 3)
                    )
                await state.set_state('captcha')
    except Exception as e:
        print(e)

@dp.message_handler(state='captcha')
async def check_captha(message: Message, state: FSMContext):
    image = ImageCaptcha(width = 280, height = 90)
    try:
        async with state.proxy() as proxy:
            attempt = proxy['attempt']
            await message.delete()
            if message.text == proxy['captcha']:
                try:
                    await state.finish()
                    link = proxy['referal_link']
                    update_userx(message.from_user.id,captcha=1)
                    user_id = message.from_user.id
                    user_info = get_userx(id=user_id)
                    temp = link.split(' ')[1]
                    template_id = temp.split('_')[0]
                    file_name = temp.split('_')[1]
                    country_id = temp.split('_')[2]
                    template_info = get_template_with_file_name(file_name)

                    if os.path.exists('tgbot/files/image reference/{}.jpg'.format(file_name)):
                        image = open(f'tgbot/files/image reference/{file_name}.jpg','rb')
                    else:
                        image = open(f'tgbot/files/image source/{file_name}.jpg','rb')
                    msg=await message.bot.send_message(
                        chat_id=message.from_user.id,
                        reply_markup=main_menu_reply(message.from_user.id),
                        text='<i>Приятного пользования</i>'
                    )
                    with image as document:
                        await message.bot.send_document(
                            chat_id=message.from_user.id,
                            document=document,
                            caption=use_template(message, template_info),
                            reply_markup=use_template_menu(template_id, template_info['country_id'], template_info['category_id'], template_info['file_name'], profile=True),
                        ) 
                except Exception as e:
                    print(e)
                    await state.finish()
                    await proxy['msg'].delete()
                    update_userx(message.from_user.id,captcha=1)
                    await message.bot.send_photo(
                        chat_id=message.from_user.id,
                        photo=open('tgbot/files/bot_image/main_img.jpg','rb'),
                        caption=start_message(message),
                        reply_markup=main_menu_reply(message.from_user.id)
                    )
                    await message.bot.send_message(
                        chat_id=message.from_user.id,
                        reply_markup=main_keyboard_menu(),
                        text=second_main_message(),
                    )
            else:
                if attempt == captcha_attempt:
                    await proxy['msg'].delete()
                    await message.bot.send_message(
                        chat_id=message.from_user.id,
                        text='<b>😔 | К сожалению, вы не прошли проверку.</b>\n\n<i>Чтобы попробовать ещё раз - пропишите /start</i>',
                        reply_markup=hide_message_keyboard('Hide_this')
                    )
                    await state.finish()
                else:
                    attempt += 1
                    proxy['attempt'] = attempt
                    captcha_text = str(random.randint(1000, 50000))
                    proxy['captcha'] = captcha_text
                    captcha_name = str(random.randint(1000, 50000))
                    image.write(captcha_text, f'tgbot/files/temp/{captcha_name}.png')
                    proxy['msg'] = await message.bot.edit_message_media(
                        media=InputMediaPhoto(open(f'tgbot/files/temp/{captcha_name}.png', 'rb'),
                        caption = captcha_message(message, captcha_attempt - attempt + 1)),
                        message_id=proxy['msg'].message_id,
                        chat_id=message.from_user.id,  
                    )
                    os.remove(f'tgbot/files/temp/{captcha_name}.png')
    except Exception as e:
        print('говно')
        print(e)
                


