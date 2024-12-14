"""Command handlers for About section."""

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from ..texts.about import (
    ABOUT_MENU_TEXT,
    MESSAGE_1_TEXT,
    MESSAGE_2_TEXT,
    MESSAGE_3_TEXT,
    TOPIC_1_TITLE,
    TOPIC_2_TITLE,
    TOPIC_3_TITLE,
)
from ..texts.commands import BACK_BTN_TEXT
from ..keyboards.about_kb import get_about_menu_kb, get_about_back_kb

# Initialize router
router = Router()

# States
class AboutStates(StatesGroup):
    """States for About section navigation."""
    main_menu = State()
    topic_1 = State()
    topic_2 = State()
    topic_3 = State()

@router.message(Command("about"))
async def cmd_about(message: types.Message, state: FSMContext) -> None:
    """
    Handle /about command - show About section menu.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(AboutStates.main_menu)
    await message.answer(
        text=ABOUT_MENU_TEXT,
        reply_markup=get_about_menu_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(AboutStates.main_menu, F.text == TOPIC_1_TITLE)
async def show_topic_1(message: types.Message, state: FSMContext) -> None:
    """
    Show Topic 1 message screen.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(AboutStates.topic_1)
    await message.answer(
        text=MESSAGE_1_TEXT,
        reply_markup=get_about_back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(AboutStates.main_menu, F.text == TOPIC_2_TITLE)
async def show_topic_2(message: types.Message, state: FSMContext) -> None:
    """
    Show Topic 2 message screen.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(AboutStates.topic_2)
    await message.answer(
        text=MESSAGE_2_TEXT,
        reply_markup=get_about_back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(AboutStates.main_menu, F.text == TOPIC_3_TITLE)
async def show_topic_3(message: types.Message, state: FSMContext) -> None:
    """
    Show Topic 3 message screen.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(AboutStates.topic_3)
    await message.answer(
        text=MESSAGE_3_TEXT,
        reply_markup=get_about_back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(F.text == "Back to topics")
async def handle_back(message: types.Message, state: FSMContext) -> None:
    """
    Handle back button navigation.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    current_state = await state.get_state()
    print(current_state)
    if current_state in [AboutStates.topic_1.state, AboutStates.topic_2.state, AboutStates.topic_3.state]:
        await cmd_about(message, state)
    elif current_state == AboutStates.main_menu.state:
        await state.clear()
        # Import here to avoid circular import
        from .start import cmd_start
        await cmd_about(message)
