"""Keyboard layouts for About section."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ..texts.commands import BACK_BTN_TEXT
from ..texts.about import TOPIC_1_TITLE, TOPIC_2_TITLE, TOPIC_3_TITLE

def get_about_menu_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard for About section main menu.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with topic buttons and back button
    """
    kb = [
        [KeyboardButton(text=TOPIC_1_TITLE)],
        [KeyboardButton(text=TOPIC_2_TITLE)],
        [KeyboardButton(text=TOPIC_3_TITLE)],
        [KeyboardButton(text=BACK_BTN_TEXT)]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_about_back_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard with back button for topic message screens.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with back button
    """
    kb = [[KeyboardButton(text="Back to topics")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
