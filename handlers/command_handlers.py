from aiogram import types
from aiogram.filters.command import Command

async def register_command_handlers(dp):
    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer("Привет")
