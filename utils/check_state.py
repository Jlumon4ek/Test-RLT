import asyncio
import logging
from aiogram import Dispatcher, Bot
from db.db import ping_server
from aiogram.exceptions import TelegramNetworkError, TelegramAPIError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def check_db_connection(retry_attempts=5):
    for attempt in range(retry_attempts):
        logger.info(f"Attempting to connect to the database, attempt {attempt + 1}")
        try:
            result = await ping_server()
            if result:
                logger.info("Successfully connected to the database.")
                return True
            else:
                logger.error(f"Attempt {attempt + 1} to connect to the database failed.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        await asyncio.sleep(2 ** attempt)
    else:
        logger.error("Max retry attempts reached. Could not connect to the database.")
        return False

async def start_bot_polling(bot: Bot, dp: Dispatcher, retry_attempts=5):
    for attempt in range(retry_attempts):
        try:
            logger.info("Start polling")
            await dp.start_polling(bot)
            logger.info("Bot started successfully.")
            return True
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
        return False
