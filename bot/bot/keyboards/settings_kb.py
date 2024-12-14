"""Settings section keyboard layouts."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from bot.texts.api_keys_list import MOCK_API_KEYS
from bot.texts.settings import BACK_TO_SETTINGS, SHOW_SUBSCRIPTIONS



def create_keyboard(buttons: List[str], rows: int = 2) -> ReplyKeyboardMarkup:
    """Create a keyboard with the specified buttons arranged in rows."""
    keyboard = []
    for i in range(0, len(buttons), rows):
        row = [KeyboardButton(text=btn) for btn in buttons[i:i + rows]]
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Main Settings Menu
def settings_main_kb() -> ReplyKeyboardMarkup:
    buttons = [
        "🔗 Referral Link",
        "📊 Monitoring",
        "💎 Subscription",
        "🔑 API Keys",
        "⬅️ Back"
    ]
    return create_keyboard(buttons)

# Subscription Menu
def subscription_kb() -> ReplyKeyboardMarkup:
    buttons = [
        "Current Plan",
        "Premium Features",
        "Buy Premium",
        BACK_TO_SETTINGS
    ]
    return create_keyboard(buttons)

# Buy Premium Menu
def buy_premium_kb() -> ReplyKeyboardMarkup:
    buttons = [
        "Telegram Stars",
        "USDT",
        "TON",
        BACK_TO_SETTINGS
    ]
    return create_keyboard(buttons)

# API Keys Menu
def api_keys_main_kb() -> ReplyKeyboardMarkup:
    buttons = [
        "🗑 Delete API Key",
        "➕ New API Key",
        BACK_TO_SETTINGS
    ]
    return create_keyboard(buttons)

def api_keys_list_kb() -> ReplyKeyboardMarkup:
    """Create keyboard with mock API keys."""
    buttons = [key["name"] for key in MOCK_API_KEYS]
    buttons.append(BACK_TO_SETTINGS)
    return create_keyboard(buttons, rows=1)

def api_key_actions_kb() -> ReplyKeyboardMarkup:
    buttons = [
        "🗑 Delete Key",
        BACK_TO_SETTINGS
    ]
    return create_keyboard(buttons)

def api_key_confirm_kb() -> ReplyKeyboardMarkup:
    buttons = [
        "Yes",
        "No",
        BACK_TO_SETTINGS
    ]
    return create_keyboard(buttons)

# Generic back button
def back_kb() -> ReplyKeyboardMarkup:
    return create_keyboard([BACK_TO_SETTINGS])

def back_to_subscriptions() -> ReplyKeyboardMarkup:
    return create_keyboard([SHOW_SUBSCRIPTIONS])