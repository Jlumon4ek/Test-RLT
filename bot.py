import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
"""Importing my modules"""
from utils.config import TOKEN
from utils.register_handlers import register_handlers
from aiogram.exceptions import TelegramServerError, TelegramNetworkError, TelegramAPIError
from db.db import ping_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await register_handlers(dp, bot)
    retry_attempts = 5
    for attempt in range(retry_attempts):
        logger.info(f"Attempting to connect to the database, attempt {attempt + 1}")
        try:
            result = await ping_server()
            if result:
                logger.info("Successfully connected to the database.")
                break
            else:
                logger.error(f"Attempt {attempt + 1} to connect to the database failed.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        await asyncio.sleep(2 ** attempt)
    else:
        logger.error("Max retry attempts reached. Could not connect to the database.")

    for attempt in range(retry_attempts):
        try:
            logger.info("Start polling")
            await dp.start_polling(bot)
            logger.info("Bot started successfully.")
            break
        except TelegramNetworkError as e:
            logger.error(f"Network error: {e}")
            await asyncio.sleep(2 ** attempt)
        except TelegramAPIError as e:
            logger.error(f"API error: {e}")
            await asyncio.sleep(2 ** attempt)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await asyncio.sleep(2 ** attempt)
    else:
        logger.error("Max retry attempts reached. Could not start bot.")

    

if __name__ == "__main__":
    asyncio.run(main())

