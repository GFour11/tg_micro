"""Command handlers for Settings section."""

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.exchanges import exchanges
from bot.core.loader import bot
from bot.core.settings import bot_config, cipher_key
from cryptography.fernet import Fernet
from bot.userservice_clients import UserMicroserviceClient

from ..texts.commands import BACK_BTN_TEXT


def get_userservice_client():
    client = UserMicroserviceClient('localhost', 5000)
    return client


from ..texts.settings import (
    SETTINGS_TITLE,
    SETTINGS_DESCRIPTION,
    API_KEYS_DELETE_CONFIRM_TEXT,
    API_KEYS_STOP_BOTS_CONFIRM_TEXT,
    NEW_API_KEY_ENTER_KEY_TEXT,
    NEW_API_KEY_EXCHANGE_TEXT,
    NEW_API_KEY_IS_INVALID_TEXT,
    REFERRAL_TITLE,
    REFERRAL_TEXT,
    MONITORING_TITLE,
    MONITORING_TEXT,
    SUBSCRIPTION_TITLE,
    CURRENT_PLAN_TEXT,
    PREMIUM_FEATURES_TEXT,
    BUY_PREMIUM_TITLE,
    PAYMENT_METHODS_TEXT,
    DEPOSIT_ADDRESS_TEXT,
    DEPOSIT_STARS_TEXT,
    API_KEYS_LIST_TEXT,
    API_KEY_DELETED_TEXT,
    NEW_API_KEY_NAME_TEXT,
    NO_API_KEYS_TEXT,
    NO_AVAILABLE_EXCHANGE_FOUND,
    ADD_KEY,
    CANCEL,
    YES,
    NO,
    KEY_RETRIEVAL_ERROR,
    ERROR_WHILE_DELETING_KEY,
    KEY_EXIST,
    DELETION_CANCELED,
    BACK_TO_SETTINGS,
    SHOW_SUBSCRIPTIONS
)
from ..keyboards.settings_kb import (
    settings_main_kb,
    subscription_kb,
    buy_premium_kb,
    back_kb, back_to_subscriptions
)

cipher = Fernet(cipher_key)


# Initialize router
router = Router()

# States
class SettingsStates(StatesGroup):
    """States for Settings section navigation."""
    main_menu = State()
    referral = State()
    monitoring = State()
    subscription = State()
    subscription_plan = State()
    subscription_features = State()
    subscription_buy = State()
    subscription_deposit = State()
    api_keys = State()
    api_keys_list = State()
    api_key_delete = State()
    api_key_stop_bots = State()
    api_key_exchange = State()
    api_key_name = State()
    api_key_key = State()
    api_key_value = State()


# Клавіатура з двома кнопками: "Мої ключі" і "Додати ключ"
def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[], row_width=2)
    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text=API_KEYS_LIST_TEXT, callback_data="my_keys")])
    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text=ADD_KEY, callback_data="add_key")])
    return keyboard


def get_confirmation_keyboard(key_id, key_name):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    yes_button = types.InlineKeyboardButton(text=YES, callback_data=f"confirm_delete:{key_id}:{key_name}")
    no_button = types.InlineKeyboardButton(text=NO, callback_data="cancel_delete")
    keyboard.inline_keyboard.append([yes_button])
    keyboard.inline_keyboard.append([no_button])
    return keyboard


def get_confirmation_keyboard_with_bots(key_id, key_name):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    yes_button = types.InlineKeyboardButton(text=YES, callback_data=f"confirm_delete_with_bots:{key_id}:{key_name}")
    no_button = types.InlineKeyboardButton(text=NO, callback_data="cancel_delete")
    keyboard.inline_keyboard.append([yes_button])
    keyboard.inline_keyboard.append([no_button])
    return keyboard


def get_cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    cancel_button = types.InlineKeyboardButton(text=CANCEL, callback_data="cancel")
    keyboard.inline_keyboard.append([cancel_button])
    return keyboard


# Клавіатура для вибору біржі
def get_exchange_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=[])

    buttons = []
    # Додаємо кнопки до клавіатури для кожної біржі
    for exchange in exchanges.keys():
        buttons.append(
            types.InlineKeyboardButton(text=exchange, callback_data=f"exchange_{exchange.lower()}")
        )
    buttons.append(types.InlineKeyboardButton(text=CANCEL, callback_data="cancel"))
    keyboard.inline_keyboard.append(buttons)
    return keyboard


@router.message(Command("settings"))
async def cmd_settings(message: types.Message, state: FSMContext) -> None:
    """
    Handle /settings command - show Settings section menu.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.set_state(SettingsStates.main_menu)
    await message.answer(
        f"{SETTINGS_TITLE}\n\n{SETTINGS_DESCRIPTION}",
        reply_markup=settings_main_kb(),
        parse_mode=ParseMode.HTML
    )
        

@router.message(SettingsStates.main_menu, F.text == "🔗 Referral Link")
async def show_referral(message: types.Message, state: FSMContext) -> None:
    """Show referral link and QR code screen."""
    await state.set_state(SettingsStates.referral)
    await message.answer(
        f"{REFERRAL_TITLE}\n\n{REFERRAL_TEXT}",
        reply_markup=back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(SettingsStates.main_menu, F.text == "📊 Monitoring")
async def show_monitoring(message: types.Message, state: FSMContext) -> None:
    """Show monitoring bot link screen."""
    await state.set_state(SettingsStates.monitoring)
    await message.answer(
        f"{MONITORING_TITLE}\n\n{MONITORING_TEXT}",
        reply_markup=back_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(SettingsStates.main_menu, F.text == "💎 Subscription")
async def show_subscription(message: types.Message, state: FSMContext) -> None:
    """Show subscription menu screen."""
    await state.set_state(SettingsStates.subscription)
    await message.answer(
        SUBSCRIPTION_TITLE,
        reply_markup=subscription_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(SettingsStates.subscription, F.text == "Current Plan")
async def show_current_plan(message: types.Message, state: FSMContext) -> None:
    """Show current subscription plan details."""
    await state.set_state(SettingsStates.subscription_plan)
    await message.answer(
        CURRENT_PLAN_TEXT,
        reply_markup=back_to_subscriptions(),
        parse_mode=ParseMode.HTML
    )

@router.message(SettingsStates.subscription, F.text == "Premium Features")
async def show_premium_features(message: types.Message, state: FSMContext) -> None:
    """Show premium features list."""
    await state.set_state(SettingsStates.subscription_features)
    await message.answer(
        PREMIUM_FEATURES_TEXT,
        reply_markup=back_to_subscriptions(),
        parse_mode=ParseMode.HTML
    )

@router.message(SettingsStates.subscription, F.text == "Buy Premium")
async def show_buy_premium(message: types.Message, state: FSMContext) -> None:
    """Show premium purchase options."""
    await state.set_state(SettingsStates.subscription_buy)
    await message.answer(
        f"{BUY_PREMIUM_TITLE}\n\n{PAYMENT_METHODS_TEXT}",
        reply_markup=buy_premium_kb(),
        parse_mode=ParseMode.HTML
    )

@router.message(SettingsStates.subscription_buy, F.text.in_(["Telegram Stars", "USDT", "TON"]))
async def show_deposit_address(message: types.Message, state: FSMContext) -> None:
    """Show deposit address for selected payment method."""
    await state.set_state(SettingsStates.subscription_deposit)
    if message.text == "Telegram Stars":
        message_text = DEPOSIT_STARS_TEXT
    else:
        message_text = DEPOSIT_ADDRESS_TEXT
    await message.answer(
        message_text,
        reply_markup=back_to_subscriptions(),
        parse_mode=ParseMode.HTML
    )


@router.message(SettingsStates.main_menu, F.text == "🔑 API Keys")
@router.callback_query(lambda c: c.data == "my_keys")
async def show_api_keys_menu(event: types.Message | types.CallbackQuery, state: FSMContext):
    is_callback = isinstance(event, types.CallbackQuery)

    client = get_userservice_client()
    response = client.send_user_data(command="list_keys", user_id=event.from_user.id)
    if response.status == "success":
        keys = response.message
        if keys:
            key_details = []
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

            for key in keys:
                key_name = key['key_name']
                key_id = key['id']
                key_details.append(f"🔑 {key_name}")
                keyboard.inline_keyboard.append(
                    [types.InlineKeyboardButton(text=f"Delete {key_name}", callback_data=f"delete_key:{key_id}:{key_name}")]
                )

            keyboard.inline_keyboard.append([types.InlineKeyboardButton(text=ADD_KEY, callback_data="add_key")])
            keys_text = "\n".join(key_details)
        else:
            keys_text = NO_API_KEYS_TEXT
            buttons=[]
            buttons.append([KeyboardButton(text=ADD_KEY)])
            buttons.append([KeyboardButton(text=BACK_TO_SETTINGS)])
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
        # Ответ пользователю
        if is_callback:
            await bot.answer_callback_query(event.id)
            await bot.send_message(event.from_user.id, keys_text, reply_markup=keyboard, parse_mode="HTML")
        else:
            await state.set_state(SettingsStates.api_keys)
            await event.answer(keys_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        error_text = KEY_RETRIEVAL_ERROR
        if is_callback:
            await bot.answer_callback_query(event.id)
            await bot.edit_message_text(error_text,
                                        chat_id=str(event.message.chat.id),
                                        message_id=str(event.message.message_id))
        else:
            await event.answer(error_text, parse_mode="HTML")


@router.message(F.text == "⬅️ Back")
async def handle_back(message: types.Message, state: FSMContext) -> None:
    """
    Handle back button navigation.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await state.clear()
    # Import here to avoid circular import
    from .start import cmd_start
    await cmd_start(message)


@router.message(F.text == "⬅️ Back to Settings")
async def handle_back_to_settings(message: types.Message, state: FSMContext) -> None:
    """
    Handle back button navigation to Settings menu.
    
    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    await cmd_settings(message, state)


# Обробка кнопки "Додати ключ"
@router.callback_query(lambda c: c.data == 'add_key')
async def add_key_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    exchanges = get_exchange_keyboard()
    if not exchanges:
        await bot.send_message(callback_query.from_user.id, NO_AVAILABLE_EXCHANGE_FOUND)
    await bot.edit_message_text(NEW_API_KEY_EXCHANGE_TEXT,
                                chat_id=str(callback_query.message.chat.id),
                                message_id=str(callback_query.message.message_id),
                                reply_markup=get_exchange_keyboard())

    await state.set_state(SettingsStates.api_key_exchange)


# FSM: Очікування вибору біржі
@router.callback_query(lambda c: c.data.startswith('exchange_'))
async def process_exchange_selection(callback_query: types.CallbackQuery, state: FSMContext):
    selected_exchange = callback_query.data.split('_')[1]  # Отримуємо вибрану біржу з callback_data

    # Видаляємо клавіатуру
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=None)

    # Зберігаємо вибрану біржу у стані FSM
    await state.update_data(selected_exchange=selected_exchange)

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(NEW_API_KEY_NAME_TEXT, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                reply_markup=get_cancel_keyboard())
    await state.set_state(SettingsStates.api_key_name)


@router.message(StateFilter(SettingsStates.api_key_name))
async def process_key_name(message: types.Message, state: FSMContext):
    key_name = message.text  # Введена користувачем назва ключа
    # Зберігаємо назву ключа у стані FSM
    await state.update_data(key_name=key_name)

    await message.answer(NEW_API_KEY_ENTER_KEY_TEXT, reply_markup=get_cancel_keyboard())
    await state.set_state(SettingsStates.api_key_value)  # Переходимо до введення значення ключа"""


# FSM: Очікування введення секрету ключа
@router.message(StateFilter(SettingsStates.api_key_value))
async def process_key_value(message: types.Message, state: FSMContext):
    key_value = message.text  # Введене користувачем значення

    # Отримуємо вибрану біржу з контексту
    user_data = await state.get_data()
    key_name = user_data.get('key_name')
    key_exchange = user_data.get('selected_exchange')
    # Шифруємо введене користувачем значення
    encrypted_key = cipher.encrypt(key_value.encode()).decode()

    # Надсилаємо запит для додавання ключа
    client = get_userservice_client()
    response = client.send_user_data(command="add_key", user_id=message.from_user.id,
                               key_data={"key": key_name, "secret": encrypted_key, "exchange": key_exchange})
    if response.status == "success":
        await message.answer(f"Key '{key_name}' is valid.", reply_markup=get_main_keyboard())
    elif response.status == "error" and response.error.error_message == "Ключ з таким іменем вже присутній":
        await message.answer(KEY_EXIST ,  reply_markup=get_main_keyboard())
    else:
        await message.answer(NEW_API_KEY_IS_INVALID_TEXT ,  reply_markup=get_main_keyboard())
    await state.clear()


@router.callback_query(lambda c: c.data == 'cancel')
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text("Adding a key has been canceled.", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                reply_markup=get_main_keyboard())


# Обробка видалення ключа
@router.callback_query(lambda c: c.data.startswith('delete_key:'))
async def delete_key_callback(callback_query: types.CallbackQuery):
    key_id = callback_query.data.split(':')[1]
    key_name = callback_query.data.split(':')[2]

    await bot.edit_message_text(API_KEYS_DELETE_CONFIRM_TEXT, chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=get_confirmation_keyboard(key_id, key_name))

    await bot.answer_callback_query(callback_query.id)


@router.callback_query(lambda c: c.data.startswith('confirm_delete:'))
async def confirm_delete_callback(callback_query: types.CallbackQuery):
    key_id = callback_query.data.split(':')[1]
    key_name = callback_query.data.split(':')[2]
    await bot.edit_message_text(API_KEYS_STOP_BOTS_CONFIRM_TEXT, chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=get_confirmation_keyboard_with_bots(key_id, key_name))
    await bot.answer_callback_query(callback_query.id)


@router.callback_query(lambda c: c.data.startswith('confirm_delete_with_bots:'))
async def confirm_delete_callback_with_keys(callback_query: types.CallbackQuery):
    key_id = callback_query.data.split(':')[1]
    key_name = callback_query.data.split(':')[2]
    # Надсилаємо запит для видалення ключа
    client = get_userservice_client()
    response = client.send_user_data(command="delete_key", user_id=callback_query.from_user.id, key_id=key_id)
    if response.status == "success":
        await bot.answer_callback_query(callback_query.id, text=API_KEY_DELETED_TEXT)
        await bot.edit_message_text(API_KEY_DELETED_TEXT,
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=get_main_keyboard())
    else:
        await bot.answer_callback_query(callback_query.id, text=ERROR_WHILE_DELETING_KEY)
        await bot.edit_message_text(ERROR_WHILE_DELETING_KEY,
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=get_main_keyboard())


@router.callback_query(lambda c: c.data.startswith('cancel_delete'))
async def cancel_delete_callback(callback_query: types.CallbackQuery):
    # Повідомляємо, що видалення скасовано
    await bot.answer_callback_query(callback_query.id, text=DELETION_CANCELED)
    await bot.send_message(callback_query.from_user.id, DELETION_CANCELED)

    await bot.send_message(callback_query.from_user.id, "Select an item from the menu.", reply_markup=get_main_keyboard())


@router.message(F.text == BACK_TO_SETTINGS)
async def handle_back_to_settings(message: types.Message, state: FSMContext) -> None:
    """
    Handle back button navigation.

    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    current_state = await state.get_state()
    await state.clear()
    # Import here to avoid circular import
    await cmd_settings(message)


@router.message(F.text == SHOW_SUBSCRIPTIONS)
async def handle_back_to_current_plan(message: types.Message, state: FSMContext) -> None:
    """
    Handle back button navigation.

    Args:
        message (types.Message): Message from user
        state (FSMContext): FSM context
    """
    current_state = await state.get_state()
    await state.set_state(SettingsStates.subscription)
    await state.clear()
    # Import here to avoid circular import
    await show_subscription(message, state)
