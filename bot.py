import asyncio
import logging
from aiogram import Bot, Dispatcher
from utils.config import TOKEN
from utils.register_handlers import register_handlers
from utils.check_state import check_db_connection, start_bot_polling


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await register_handlers(dp)

    db_connected = await check_db_connection()
    if not db_connected:
        return

    bot_started = await start_bot_polling(bot, dp)
    if not bot_started:
        return

if __name__ == "__main__":
    asyncio.run(main())
