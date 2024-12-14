"""Bot initialization and core components loader."""

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from .settings import bot_config

# Initialize bot and dispatcher
bot = Bot(
    token=bot_config.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Create __init__.py to make it a package
__all__ = ["bot", "dp"]
