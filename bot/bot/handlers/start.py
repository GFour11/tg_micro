"""Command handlers for main menu commands."""

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
# from ..userservice_clients import UserMicroserviceClient

from ..texts.commands import (
    MAIN_MENU_TEXT,
    BACK_BTN_TEXT,
)

# Initialize router
router = Router()

# def get_userservice_client():
#     client = UserMicroserviceClient('userservice', 5000)
#     return client


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """
    Handle /start command - show main menu.
    
    Args:
        message (types.Message): Message from user
    """
    command_text = message.text.strip()  # Убираем лишние пробелы
    if len(command_text.split()) > 1:
        referral_code = command_text.split()[1]  # Получаем аргумент после команды
    else:
        referral_code = None
    # client = get_userservice_client()
    # response = client.send_user_data(
    #     command="get_or_create",
    #     user_id=message.from_user.id,
    #     user_data={
    #         "first_name": message.from_user.first_name,
    #         "last_name": message.from_user.last_name,
    #         "username": message.from_user.username},
    #     referral_code=referral_code
    # )

    await message.answer(
        text=MAIN_MENU_TEXT,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(lambda message: message.text == BACK_BTN_TEXT)
@router.callback_query(lambda c: c.data == "back_to_main_menu")
async def back_to_main_menu(message: types.Message) -> None:
    """
    Handle back button - return to main menu.
    
    Args:
        message (types.Message): Message from user
    """
    await cmd_start(message)
