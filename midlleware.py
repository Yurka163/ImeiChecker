from config_reader import config
from aiogram import BaseMiddleware

white_list = config.white_list


class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = data["event_from_user"]
        if user_id.id not in white_list:
            await event.message.answer(f"Доступ запрещен!")
            return
        else:
            return await handler(event, data)
