# - *- coding: utf- 8 - *-
from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.utils.exceptions import Throttled

from tgbot.data.config import get_admins


# Мидлварь для антиспама
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict):
        try:
            handler = current_handler.get()
            dispatcher = Dispatcher.get_current()

            if handler:
                limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
                key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
            else:
                limit = self.rate_limit
                key = f"{self.prefix}_message"

            if message.from_user.id not in get_admins():
                try:
                    await dispatcher.throttle(key, rate=limit)
                except Throttled as t:
                    await self.message_throttled(message, t)
                    raise CancelHandler()
        except Exception as e:
            print(e)

    @staticmethod
    async def message_throttled(message: types.Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            try:
                await message.reply("<b>❗ Не спамь или дам по жопе.</b>")
            except Exception as e:
                print(e)


# Изменение лимитов отправки сообщения у декораторов
def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator
