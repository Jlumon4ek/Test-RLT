from handlers.command_handlers import register_command_handlers
from handlers.message_handlers import register_message_handlers


async def register_handlers(dp, bot):
    await register_command_handlers(dp, bot)
    await register_message_handlers(dp, bot)

