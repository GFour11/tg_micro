"""Main entry point for the Telegram bot."""

import asyncio
import logging
from aiogram import types

from bot.core.loader import bot, dp
from bot.core.settings import bot_config
from bot.handlers.start import router as start_router
from bot.handlers.about import router as about_router
from bot.handlers.dashboard import router as dashboard_router
from bot.handlers.settings import router as settings_router
from bot.handlers.bots import router as bots_router
from bot.texts.commands import COMMANDS_DESCRIPTION


async def set_commands():
    """Set bot commands in the menu."""
    await bot.set_my_commands([
        types.BotCommand(command=command, description=description)
        for command, description in COMMANDS_DESCRIPTION.items()
    ])

async def main():
    """Main function to start the bot."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Check if bot is configured
    if not bot_config.is_configured:
        logging.error("Bot token not found. Please set BOT_TOKEN in .env file")
        return

    # Include routers
    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(dashboard_router)
    dp.include_router(settings_router)
    dp.include_router(bots_router)

    # Set bot commands
    await set_commands()

    # Start polling
    logging.info("Bot started")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
