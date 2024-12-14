"""Keyboard layouts for different menus."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ..texts.commands import BACK_BTN_TEXT

def get_about_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard for About section.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with back button
    """
    kb = [[KeyboardButton(text=BACK_BTN_TEXT)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_dashboard_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard for Dashboard section.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with back button
    """
    kb = [[KeyboardButton(text=BACK_BTN_TEXT)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_bots_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard for Bots Management section.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with back button
    """
    kb = [[KeyboardButton(text=BACK_BTN_TEXT)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_settings_kb() -> ReplyKeyboardMarkup:
    """
    Create keyboard for Settings section.
    
    Returns:
        ReplyKeyboardMarkup: Keyboard with back button
    """
    kb = [[KeyboardButton(text=BACK_BTN_TEXT)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
