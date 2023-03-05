# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.data.config import get_admins, get_sub_links
from tgbot.keyboards.inline_all import sub_keyboard
from tgbot.messages.msg import is_still_sub_message

# Мидлварь для антиспама
class IsStillSubMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(IsStillSubMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict):
        try:
            for chat_id in get_sub_links():
                sub = await message.bot.get_chat_member(
                    chat_id=chat_id,
                    user_id=message.from_user.id
                )
                if message.from_user.id not in get_admins() and 'start' not in message.text and str(sub.status) == 'left':
                    try:
                        await self.still_sub_func(message)
                        raise CancelHandler()
                    except Exception as e:
                        raise LifetimeControllerMiddleware('not sub')
        except Exception as e:
            raise LifetimeControllerMiddleware('not sub')

    @staticmethod
    async def still_sub_func(message: types.Message):
        try:
            await message.bot.send_message(
                text=is_still_sub_message(message),
                chat_id=message.from_user.id,
                reply_markup=sub_keyboard(),
                )
        except Exception as e:
            print(e)
