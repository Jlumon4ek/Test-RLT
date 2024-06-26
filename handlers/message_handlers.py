from aiogram import types, Dispatcher, Bot
from db.db import get_by_date
from utils.validators import is_valid_message, parse_message

async def json_message_handler(message: types.Message):
    if await is_valid_message(message.text):
        data = parse_message(message.text)
        result = await get_by_date(data.dt_from, data.dt_upto, data.group_type)
        await message.answer(f"{result}")
    else:
        await message.answer("Неверный формат сообщения.")

async def register_message_handlers(dp: Dispatcher):
    dp.message.register(json_message_handler)
