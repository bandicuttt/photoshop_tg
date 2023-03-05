# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from tgbot.keyboards.inline_all import sub_keyboard
from tgbot.messages.msg import sub_message

from tgbot.services.api_sqlite import get_userx
from tgbot.data.config import get_admins, get_sub_links
from tgbot.data.loader import dp, bot


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        try:
            if message.from_user.id in get_admins():
                return True
            else:
                return False
        except Exception as e:
            print(e)

class IsSubMessage(BoundFilter):
    async def check(self, message: types.Message):
        try:
            for chat_id in get_sub_links():
                sub = await bot.get_chat_member(
                    chat_id=chat_id,
                    user_id=message.from_user.id
                )
                if str(sub.status) != 'left':
                    return True
                else:
                    await dp.bot.send_message(
                        chat_id=message.from_user.id,
                        reply_markup=sub_keyboard(),
                        text=sub_message(message)
                    )
        except Exception as e:
            print(e)
