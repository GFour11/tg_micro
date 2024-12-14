"""Keyboard layouts for bot management."""

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.texts.bots import BOT_TYPES, SIGNAL_TYPES, BACK_TO_BOTS

# def get_bots_main_menu() -> ReplyKeyboardMarkup:
#     """
#     Creates the main bots menu keyboard.
    
#     Returns:
#         ReplyKeyboardMarkup: Main bots menu keyboard
#     """
#     kb = ReplyKeyboardBuilder()
#     kb.button(text="📋 Your Bots")
#     kb.button(text="➕ New Bot")
#     kb.button(text=BACK_TO_BOTS)
#     kb.adjust(2)
#     return kb.as_markup(resize_keyboard=True)

def get_bot_type_keyboard() -> InlineKeyboardMarkup:
   """
   Creates keyboard for bot type selection.
   
   Returns:
       InlineKeyboardMarkup: Bot type selection keyboard
   """
   keyboard = InlineKeyboardBuilder()
   for bot_type in BOT_TYPES.values():
       keyboard.button(text=bot_type, callback_data=bot_type)
   keyboard.button(text=BACK_TO_BOTS, callback_data=BACK_TO_BOTS)
   keyboard.adjust(1)
   return keyboard.as_markup()

def get_signal_or_classic_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates keyboard for signal or classic bot selection.
    
    Returns:
        ReplyKeyboardMarkup: Signal or classic bot selection keyboard
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="Signal Bot")
    kb.button(text="Classic Bot")
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_signal_type_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates keyboard for signal type selection.
    
    Returns:
        ReplyKeyboardMarkup: Signal type selection keyboard
    """
    kb = ReplyKeyboardBuilder()
    for signal in SIGNAL_TYPES.values():
        kb.button(text=signal)
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_exchange_and_quote_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates keyboard for exchange and quote selection.
    
    Returns:
        ReplyKeyboardMarkup: Exchange and quote selection keyboard
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="Exchange")
    kb.button(text="Choose quote")
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_bots_keyboard(page: int, total_bots: int):
    # Number of bots per page
    bots_per_page = 10

    # Calculate the starting and ending index for the current page
    start_index = (page - 1) * bots_per_page
    end_index = min(start_index + bots_per_page, total_bots)

    # Create a keyboard layout
    keyboard = InlineKeyboardBuilder()

    # Generate bot index buttons
    for i in range(start_index, end_index):
        keyboard.button(text=str(i + 1), callback_data=f'bot_{i}')
    
    if page > 1:
        keyboard.button(text="◀️", callback_data=f'prev_{page - 1}')
    # else:
    #     keyboard.button(text=" ", callback_data="ignore")
    
    keyboard.button(text="+ New", callback_data="new_bot")
    keyboard.button(text="❌", callback_data="close_bots_list")
    
    if end_index < total_bots:
        keyboard.button(text="▶️", callback_data=f'next_{page + 1}')
    # else:
    #     keyboard.button(text=" ", callback_data="ignore")
    keyboard.adjust(5)

    return keyboard.as_markup()


def get_bot_management_keyboard(bot_id: str) -> InlineKeyboardMarkup:
    """
    Creates inline keyboard for bot management options.

    Args:
        bot_id: ID of the bot being managed

    Returns:
        InlineKeyboardMarkup: Bot management inline keyboard
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Edit Bot", callback_data=f"⚙️ Edit Bot")],
        [InlineKeyboardButton(text="⏹ Stop Bot", callback_data=f"⏹ Stop Bot")],
        [InlineKeyboardButton(text="⬅️ Back to Bots", callback_data="⬅️ Back to Bots")]
    ])

def get_api_key_confirmation_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates confirmation keyboard for bot actions.
    
    Returns:
        ReplyKeyboardMarkup: Confirmation keyboard
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="✅ Confirm")
    kb.button(text="❌ Error")
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_strategy_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates keyboard for strategy selection.
    
    Returns:
        ReplyKeyboardMarkup: Strategy selection keyboard
    """
    kb = ReplyKeyboardBuilder()
    strategies = [
        "Launch",
        "Advanced Setup"
    ]
    for strategy in strategies:
        kb.button(text=strategy)
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_advanced_setup_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates keyboard for advanced bot setup options.
    
    Returns:
        ReplyKeyboardMarkup: Advanced setup keyboard
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="Stop-loss type")
    kb.button(text="Lot multiplier")
    kb.button(text="Step delta")
    kb.button(text="Lot size")
    kb.button(text="Saver")
    kb.button(text="Cover rate")
    kb.button(text="Profit reinvest")
    kb.button(text="Loss reinvest")
    kb.button(text="Stopping")
    kb.button(text="Add to portfolio")
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_portfolio_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates keyboard for portfolio management options.
    
    Returns:
        ReplyKeyboardMarkup: Portfolio management keyboard
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="New portfolio")
    kb.button(text="Select portfolio")
    kb.button(text=BACK_TO_BOTS)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_mock_api_key() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="My key (mock_key_12345)")
    return kb.as_markup(resize_keyboard=True)