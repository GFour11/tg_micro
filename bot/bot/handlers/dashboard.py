"""Command handlers for Dashboard section."""

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from ..texts.dashboard import (
    DASHBOARD_MENU_TEXT,
    REFERRALS_TEXT,
    PORTFOLIO_TEXT,
    BACKTESTS_TEXT,
    REFERRALS_TITLE,
    PORTFOLIO_TITLE,
    BACKTESTS_TITLE,
)
from ..texts.commands import BACK_BTN_TEXT
from ..keyboards.dashboard_kb import get_dashboard_menu_kb, get_dashboard_back_kb

# Initialize router
router = Router()

# States
class DashboardStates(StatesGroup):
    """States for Dashboard section navigation."""
    main_menu = State()
    referrals = State()
    portfolio = State()
    backtests = State()

@router.message(Command("dashboard"))
async def cmd_dashboard(message: types.Message, state: FSMContext) -> None:
    """
    Handle /dashboard command - show Dashboard section menu.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(DashboardStates.main_menu)
    await message.answer(
        text=DASHBOARD_MENU_TEXT,
        reply_markup=get_dashboard_menu_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(DashboardStates.main_menu, F.text == REFERRALS_TITLE)
async def show_referrals(message: types.Message, state: FSMContext) -> None:
    """
    Show Referrals screen.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(DashboardStates.referrals)
    await message.answer(
        text=REFERRALS_TEXT,
        reply_markup=get_dashboard_back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(DashboardStates.main_menu, F.text == PORTFOLIO_TITLE)
async def show_portfolio(message: types.Message, state: FSMContext) -> None:
    """
    Show Portfolio screen.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(DashboardStates.portfolio)
    await message.answer(
        text=PORTFOLIO_TEXT,
        reply_markup=get_dashboard_back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(DashboardStates.main_menu, F.text == BACKTESTS_TITLE)
async def show_backtests(message: types.Message, state: FSMContext) -> None:
    """
    Show Backtests screen.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(DashboardStates.backtests)
    await message.answer(
        text=BACKTESTS_TEXT,
        reply_markup=get_dashboard_back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(F.text == "BACK TO DASHBOARD")
async def handle_back(message: types.Message, state: FSMContext) -> None:
    """
    Handle back button navigation.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    current_state = await state.get_state()
    
    if current_state in [
        DashboardStates.referrals.state,
        DashboardStates.portfolio.state,
        DashboardStates.backtests.state
    ]:
        await cmd_dashboard(message, state)
    elif current_state == DashboardStates.main_menu.state:
        await state.clear()
        # Import here to avoid circular import
        from .start import cmd_start
        await cmd_start(message)
