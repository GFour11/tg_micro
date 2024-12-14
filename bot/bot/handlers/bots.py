"""Command handlers for bots management."""

from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from bot.handlers.start import cmd_start
from bot.handlers.settings import show_api_keys_menu
from bot.keyboards import bots_kb
from bot.keyboards import settings_kb
from bot.handlers.settings import SettingsStates
from bot.texts import bots as texts
from bot.texts.api_keys_list import MOCK_API_KEYS
from bot.texts.bots_list import MOCK_BOTS
from bot.core.user_messages import user_messages
from bot.utils.calendar import CalendarKeyboard
from ..texts.settings import (
BUY_PREMIUM_TITLE, PAYMENT_METHODS_TEXT)



router = Router()

# States for bot creation flow
class BotCreation(StatesGroup):
    selecting_type = State()
    select_signal_or_classic = State()
    start_date = State()
    end_date = State()
    signal_type = State()
    add_bot_name = State()
    exchange_or_qoute = State()
    choose_quote = State()
    max_total_balance = State()
    exchange = State()
    symbol = State()
    max_balance = State()
    max_active_bots = State()
    profit_target = State()
    max_risk = State()
    price_limit = State()
    strategy = State()
    portfolio = State()
    new_portfolio = State()
    launch = State()
    advanced_setup = State()
    api_key = State()
    next = State()
    confirmation = State()

class BotViewing(StatesGroup):
    viewing_bot = State()

# Main menu handler
@router.message(Command("bots"))
async def show_bots_menu(message: Message, page: int = 1):
    bots = MOCK_BOTS
    bots_per_page = 10
    total_bots = len(bots)

    # Calculate the starting and ending index for the current page
    start_index = (page - 1) * bots_per_page
    end_index = min(start_index + bots_per_page, total_bots)

    # Generate the message text with numerated bots
    bot_list_text = ""
    for i in range(start_index, end_index):
        bot_status = bots[i]['status']
        bot_list_text += f"{i + 1}. {bots[i]['name']} - {bot_status}\n"

    # Send the message with the bot list and the keyboard
    await message.answer(bot_list_text, reply_markup=bots_kb.get_bots_keyboard(page, total_bots))

# BACK button handler for reply keyboards
@router.message(F.text == texts.BACK_TO_BOTS)
async def back_to_bot_list(message: Message, state: FSMContext):
    """Handler for returning to bot list"""
    start_page = 1
    await state.clear()
    await show_bots_menu(message, start_page)
    
# BACK button handler for inline keyboards
@router.callback_query(lambda c: c.data and c.data == texts.BACK_TO_BOTS)
async def back_to_bot_list_callback(callback: CallbackQuery, state: FSMContext):
    """Handler for returning to bot list"""
    await state.clear()
    start_page = 1
    await show_bots_menu(callback.message, start_page)

# New bot creation handler
@router.message(F.text == "➕ New Bot")
async def start_bot_creation(message: Message, state: FSMContext):
    """Handler for starting bot creation process"""
    await state.set_state(BotCreation.selecting_type)
    await message.answer(
        texts.SELECT_BOT_TYPE,
        reply_markup=bots_kb.get_bot_type_keyboard(),
        parse_mode="HTML"
    )

# New bot creation handler for inline keyboards
@router.callback_query(lambda c: c.data and c.data == "new_bot")
async def start_bot_creation_callback(callback: CallbackQuery, state: FSMContext):
    """Handler for starting bot creation process"""
    await state.set_state(BotCreation.selecting_type)
    await callback.message.answer(
        texts.SELECT_BOT_TYPE,
        reply_markup=bots_kb.get_bot_type_keyboard(),
        parse_mode="HTML"
    )

# Callback handler for pagination and bot selection
@router.callback_query(lambda c: c.data and c.data.startswith(('prev_', 'next_', 'bot_')))
async def bot_callback_handler(callback_query: CallbackQuery):
    data = callback_query.data
    
    if data.startswith('prev_'):
        page = int(data.split('_')[1])
        await show_bots_menu(callback_query.message, page)
    elif data.startswith('next_'):
        page = int(data.split('_')[1])
        await show_bots_menu(callback_query.message, page)
    elif data.startswith('bot_'):
        bot_index = int(data.split('_')[1])
        bot = MOCK_BOTS[bot_index]

        await callback_query.message.answer(
            f"<b>Bot Details:</b>\n"
            f"Name: {bot['name']}\n"
            f"Type: {bot['type']}\n"
            f"Status: {bot['status']}",
            reply_markup=bots_kb.get_bot_management_keyboard(bot["id"]),
            parse_mode="HTML"
        )
    await callback_query.answer()
    
# Handler for bot list closing and return to main menu
@router.callback_query(lambda c: c.data and c.data == "close_bots_list")
async def cancel_calendar(callback: CallbackQuery, state: FSMContext):
    """Handler for calendar cancel button"""
    await callback.message.delete()
    await callback.answer()
    await state.clear()
    await cmd_start(callback.message)

@router.callback_query(lambda callback: callback.data == "⚙️ Edit Bot")
async def edit_bot(callback: CallbackQuery, state: FSMContext):
    """Handler for editing a bot"""
    data = await state.get_data()
    bot_id = data.get("current_bot_id")
    bot = next((b for b in MOCK_BOTS if b["id"] == bot_id), None)
    if bot:
        await state.set_state(BotCreation.symbol)
        await state.update_data(bot_id=bot_id)
        await callback.message.edit_text(
            texts.ENTER_SYMBOL,
            parse_mode="HTML"
        )
        await callback.answer()
    else:
        await callback.message.edit_text(
            "Create bot edit logic later."
        )
        await callback.answer()

@router.callback_query(lambda callback: callback.data == "⏹ Stop Bot")
async def stop_bot(callback: CallbackQuery, state: FSMContext):
    """Handler for stopping a bot"""
    await callback.message.edit_text(
        "Create stop logic later."
    )
    await callback.answer()
    await state.clear()
    # await message.answer(
    #     texts.BOT_STOPPED,
    #     reply_markup=bots_kb.get_bot_list_keyboard(),
    #     parse_mode="HTML"
    # )
    await state.clear()

# Bot type selection handlers for callback queries
@router.callback_query(BotCreation.selecting_type, F.data.in_(texts.BOT_TYPES.values()))
async def process_bot_type(callback: CallbackQuery, state: FSMContext):
    """Handler for bot type selection"""
    user_data = await state.get_data()
    is_premium = user_data.get("is_premium", False) #<--------- Надалі,
    # як працюватиме мікросервіс і бд - реалізувати логіку перевірки преміум статуса
    if not is_premium:

        await state.set_state(SettingsStates.subscription_buy)
        await callback.message.answer(
            f"{BUY_PREMIUM_TITLE}\n\n{PAYMENT_METHODS_TEXT}",
            reply_markup=settings_kb.buy_premium_kb(),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    await state.update_data(bot_type=callback.data)

    if "Backtesting" in callback.data:

        await state.set_state(BotCreation.start_date)
        now = datetime.now()
        calendar = CalendarKeyboard.create_calendar(now.year, now.month)
        await callback.message.answer(
            texts.SELECT_START_DATE,
            reply_markup=calendar,
            parse_mode="HTML"
        )
    elif "Virtual" in callback.data or "Real" in callback.data:
        await state.set_state(BotCreation.select_signal_or_classic)
        await callback.message.answer(
            texts.SELECT_SIGNAL_OR_CLASSIC,
            reply_markup=bots_kb.get_signal_or_classic_keyboard(),
            parse_mode="HTML"
        )
    await callback.answer()
    
# Signal or classic bot handlers
@router.message(BotCreation.select_signal_or_classic, F.text == "Signal Bot")
async def process_signal_bot(message: Message, state: FSMContext):
    """Handler for signal bot selection"""
    await state.set_state(BotCreation.signal_type)
    await message.answer(
        texts.SELECT_SIGNAL,
        reply_markup=bots_kb.get_signal_type_keyboard(),
        parse_mode="HTML"
    )
    
@router.message(BotCreation.select_signal_or_classic, F.text == "Classic Bot")
async def process_classic_bot(message: Message, state: FSMContext):
    """Handler for classic bot selection"""
    await state.set_state(BotCreation.exchange)
    await message.answer(
        texts.ENTER_EXCHANGE,
        parse_mode="HTML"
    )

# Calendar handlers
@router.callback_query(lambda c: c.data and c.data.startswith("calendar"))
async def process_calendar(callback: CallbackQuery, state: FSMContext):
    """Handler for calendar interactions"""
    current_state = await state.get_state()
    
    if "select" in callback.data:
        date = CalendarKeyboard.process_selection(callback.data)
        if not date:
            await callback.answer(texts.INVALID_DATE)
            return
            
        if current_state == BotCreation.start_date:
            await state.update_data(start_date=date)
            await state.set_state(BotCreation.end_date)
            now = datetime.now()
            calendar = CalendarKeyboard.create_calendar(now.year, now.month)
            await callback.message.edit_text(
                texts.SELECT_END_DATE,
                reply_markup=calendar,
                parse_mode="HTML"
            )
        elif current_state == BotCreation.end_date:
            await state.update_data(end_date=date)
            await state.set_state(BotCreation.select_signal_or_classic)
            await callback.message.answer(
                texts.SELECT_SIGNAL_OR_CLASSIC,
                reply_markup=bots_kb.get_signal_or_classic_keyboard(),
                parse_mode="HTML"
            )
    
    elif "prev" in callback.data or "next" in callback.data:
        parts = callback.data.split(":")
        year = int(parts[2])
        month = int(parts[3])
        
        if "prev" in callback.data:
            year, month = CalendarKeyboard.get_prev_month(year, month)
        else:
            year, month = CalendarKeyboard.get_next_month(year, month)
            
        calendar = CalendarKeyboard.create_calendar(year, month)
        await callback.message.edit_reply_markup(reply_markup=calendar)
        
    await callback.answer()

# Signal type handlers
@router.message(BotCreation.signal_type, F.text.in_(texts.SIGNAL_TYPES.values()))
async def process_signal_type(message: Message, state: FSMContext):
    """Handler for signal type selection"""
    await state.update_data(signal_type=message.text)
    await state.set_state(BotCreation.add_bot_name)
    
    if "TradingView" in message.text:
        await message.answer(
            texts.HOW_TO_SETUP_ALERT,
            parse_mode="HTML"
        )
    
    await message.answer(
        texts.ENTER_BOT_NAME,
        parse_mode="HTML"
    )
    
# Bot name handler
@router.message(BotCreation.add_bot_name)
async def process_bot_name(message: Message, state: FSMContext):
    """Handler for bot name input"""
    await state.update_data(name=message.text)
    await state.set_state(BotCreation.exchange_or_qoute)
    await message.answer(
        texts.SETUP_EXCHAGE_OR_QUOTE,
        reply_markup=bots_kb.get_exchange_and_quote_keyboard(),
        parse_mode="HTML"
    )
    
# Exchange and quote handlers
@router.message(BotCreation.exchange_or_qoute, F.text == "Exchange")
async def process_exchange_setup(message: Message, state: FSMContext):
    """Handler for exchange setup"""
    await state.set_state(BotCreation.exchange_or_qoute)
    await message.answer(
        texts.ENTER_EXCHANGE,
        parse_mode="HTML"
    )
    
@router.message(BotCreation.exchange_or_qoute, F.text == "Choose quote")
async def process_quote_setup(message: Message, state: FSMContext):
    """Handler for quote setup"""
    await state.set_state(BotCreation.choose_quote)
    await message.answer(
        texts.ENTER_QUOTE,
        parse_mode="HTML"
    )
    
@router.message(BotCreation.exchange_or_qoute, F.text.not_in(["Exchange", "Choose quote"]))
async def process_quote_setup_after_exchange(message: Message, state: FSMContext):
    """Handler for quote setup"""
    await state.set_state(BotCreation.choose_quote)
    await message.answer(
        texts.ENTER_QUOTE,
        parse_mode="HTML"
    )

@router.message(BotCreation.choose_quote)
async def process_quote(message: Message, state: FSMContext):
    """Handler for quote input"""
    await state.update_data(quote=message.text)
    await state.set_state(BotCreation.max_total_balance)
    await message.answer(
        texts.ENTER_MAX_TOTAL_BALANCE,
        parse_mode="HTML"
    )
    
# Max total balance and max active bots handlers
@router.message(BotCreation.max_total_balance)
async def process_max_total_balance(message: Message, state: FSMContext):
    """Handler for max total balance input"""
    try:
        balance = float(message.text)
        if balance <= 0:
            raise ValueError
        
        await state.update_data(max_total_balance=balance)
        await state.set_state(BotCreation.max_active_bots)
        await message.answer(
            texts.MAX_ACTIVE_BOTS_PER_SYMBOL,
            parse_mode="HTML"
        )
    except ValueError:
        await message.answer(
            texts.INVALID_BALANCE,
            parse_mode="HTML"
        )
        
@router.message(BotCreation.max_active_bots)
async def process_max_active_bots(message: Message, state: FSMContext):
    """Handler for max active bots input"""
    try:
        bots = int(message.text)
        if bots <= 0:
            raise ValueError
        
        await state.update_data(max_active_bots=bots)
        await state.set_state(BotCreation.max_balance)
        await message.answer(
            texts.ENTER_MAX_BALANCE,
            parse_mode="HTML"
        )
    except ValueError:
        await message.answer(
            texts.INVALID_BALANCE,
            parse_mode="HTML"
        )

# Exchange and symbol handlers
@router.message(BotCreation.exchange)
async def process_exchange(message: Message, state: FSMContext):
    """Handler for exchange input"""
    await state.update_data(exchange=message.text)
    await state.set_state(BotCreation.symbol)
    await message.answer(
        texts.ENTER_SYMBOL,
        parse_mode="HTML"
    )

@router.message(BotCreation.symbol)
async def process_symbol(message: Message, state: FSMContext):
    """Handler for symbol input"""
    if "/" not in message.text:
        await message.answer(
            texts.INVALID_SYMBOL,
            parse_mode="HTML"
        )
        return
        
    await state.update_data(symbol=message.text)
    await state.set_state(BotCreation.max_balance)
    await message.answer(
        texts.ENTER_MAX_BALANCE,
        parse_mode="HTML"
    )

# Balance and risk handlers
@router.message(BotCreation.max_balance)
async def process_max_balance(message: Message, state: FSMContext):
    """Handler for max balance input"""
    try:
        balance = float(message.text)
        if balance <= 0:
            raise ValueError
        await state.update_data(max_balance=balance)
        await state.set_state(BotCreation.profit_target)
        await message.answer(
            texts.ENTER_PROFIT_TARGET,
            parse_mode="HTML"
        )
    except ValueError:
        await message.answer(
            texts.INVALID_BALANCE,
            parse_mode="HTML"
        )

@router.message(BotCreation.profit_target)
async def process_profit_target(message: Message, state: FSMContext):
    """Handler for profit target input"""
    try:
        target = float(message.text)
        if not 0 < target <= 100:
            raise ValueError
        await state.update_data(profit_target=target)
        await state.set_state(BotCreation.max_risk)
        await message.answer(
            texts.ENTER_MAX_RISK,
            parse_mode="HTML"
        )
    except ValueError:
        await message.answer(
            texts.INVALID_PERCENTAGE,
            parse_mode="HTML"
        )

@router.message(BotCreation.max_risk)
async def process_max_risk(message: Message, state: FSMContext):
    """Handler for max risk input"""
    try:
        risk = float(message.text)
        if not 0 < risk <= 100:
            raise ValueError
        await state.update_data(max_risk=risk)
        await state.set_state(BotCreation.price_limit)
        await message.answer(
            texts.ENTER_PRICE_LIMIT,
            parse_mode="HTML"
        )
    except ValueError:
        await message.answer(
            texts.INVALID_PERCENTAGE,
            parse_mode="HTML"
        )
        
@router.message(BotCreation.price_limit)
async def process_price_limit(message: Message, state: FSMContext):
    """Handler for price limit input"""
    await state.update_data(price_limit=message.text)
    await state.set_state(BotCreation.strategy)
    await message.answer(
        texts.SELECT_STRATEGY,
        reply_markup=bots_kb.get_strategy_keyboard(),
        parse_mode="HTML"
    )
        
@router.message(BotCreation.strategy, F.text == "Launch")
async def launch_bot(message: Message, state: FSMContext):
    """Handler for launching bot without advanced setup"""
    # Check if user have API keys
    # If not, redirect to API keys setup
    await state.set_state(BotCreation.launch)
    try:
        await show_api_keys_menu(message, state)
    except:
        await state.set_state(BotCreation.next)
        await message.answer(
            texts.SELECT_API_KEY,
            reply_markup=bots_kb.get_mock_api_key())
    


@router.message(BotCreation.next)
async def api_key(message: Message, state: FSMContext):
    """Handler for launching api key in bot """

    await state.set_state(BotCreation.confirmation)
    await message.answer(
        "Confirm or decline",
        reply_markup=bots_kb.get_api_key_confirmation_keyboard(),
        parse_mode="HTML"
    )


# Advanced setup handlers
@router.message(BotCreation.strategy, F.text == "Advanced Setup")
async def advanced_setup(message: Message, state: FSMContext):
    """Handler for advanced setup selection"""
    await state.set_state(BotCreation.advanced_setup)
    await message.answer(
        texts.ADVANCED_SETUP,
        reply_markup=bots_kb.get_advanced_setup_keyboard(),
        parse_mode="HTML"
    )
    
@router.message(BotCreation.advanced_setup, F.text == "Add to portfolio")
async def add_to_portfolio(message: Message, state: FSMContext):
    """Handler for adding bot to portfolio"""
    await state.set_state(BotCreation.portfolio)
    await message.answer(
        texts.PORTFOLIO_SETTINGS,
        reply_markup=bots_kb.get_portfolio_keyboard(),
        parse_mode="HTML"
    )
    
@router.message(BotCreation.portfolio, F.text == "New portfolio")
async def new_portfolio(message: Message, state: FSMContext):
    """Handler for creating a new portfolio"""
    await state.set_state(BotCreation.new_portfolio)
    await message.answer(
        texts.NEW_PORTFOLIO,
        parse_mode="HTML"
    )
    
@router.message(BotCreation.new_portfolio)
async def process_new_portfolio(message: Message, state: FSMContext):
    """Handler for new portfolio name input"""
    await state.update_data(portfolio=message.text)
    await state.clear_state()
    await show_bots_menu(message, state)

# Confirmation handlers
@router.message(BotCreation.confirmation, F.text == "✅ Confirm")
async def confirm_bot_creation(message: Message, state: FSMContext):
    """Handler for confirming bot creation"""
    await message.answer(
        texts.BOT_CREATED,
        parse_mode="HTML"
    )
    await cmd_start(message)
    # await state.clear()
    # # Return to bots menu after creation
    # await show_bots_menu(message, state)

@router.message(BotCreation.confirmation, F.text.in_(["❌ Cancel", "❌ Error"]))
async def cancel_bot_creation(message: Message, state: FSMContext):
    """Handler for canceling bot creation"""
    await state.clear()
    await show_bots_menu(message, state)
