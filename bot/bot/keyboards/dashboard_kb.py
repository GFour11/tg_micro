"""Keyboard layouts for Dashboard section."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ..texts.commands import BACK_BTN_TEXT
from ..texts.dashboard import REFERRALS_TITLE, PORTFOLIO_TITLE, BACKTESTS_TITLE

def get_dashboard_menu_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard for Dashboard section main menu.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with dashboard options and back button
    """
    kb = [
        [KeyboardButton(text=REFERRALS_TITLE)],
        [KeyboardButton(text=PORTFOLIO_TITLE)],
        [KeyboardButton(text=BACKTESTS_TITLE)],
        [KeyboardButton(text=BACK_BTN_TEXT)]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_dashboard_back_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard with back button for dashboard option screens.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with back button
    """
    kb = [[KeyboardButton(text="BACK TO DASHBOARD")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
