from aiogram import types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.fsm.context import FSMContext


async def register_command_handlers(dp, bot):
    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer("Привет")
