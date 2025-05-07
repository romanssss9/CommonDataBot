from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from keyboards import buttons, profile_kb, cancel_profile_kb
import re

from database import (
    update_user_email,
    update_user_phone,
    get_user
)

router = Router()

# Состояния FSM
class ProfileStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()

# Форматированные данные пользователя
def format_user_profile(user_data):
    if not user_data:
        return "Профиль не найден."
    return (
        f"👤 Имя: {user_data['first_name']}\n"
        f"🆔 Telegram ID: {user_data['telegram_id']}\n"
        f"📧 Email: {user_data['email'] or 'не указан'}\n"
        f"📱 Телефон: {user_data['phone'] or 'не указан'}\n"
        f"💼 Подписка активна: {'Да' if user_data['is_subscription'] else 'Нет'}"
    )


# Для обычного текстового сообщения "Профиль" или команды /profile
@router.message(F.text == buttons['profile'])
@router.message(Command('profile'))
async def show_profile_message(message: Message, state: FSMContext):
    await state.clear()
    user_data = get_user(message.from_user.id)
    await message.answer(format_user_profile(user_data), reply_markup=profile_kb)

# Для инлайн-кнопки "⬅️ Назад"
@router.callback_query(F.data == "show_profile")
async def show_profile_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = get_user(callback.from_user.id)
    await callback.message.edit_text(format_user_profile(user_data), reply_markup=profile_kb)
    await callback.answer()

    
# Обработка нажатия на "Добавить email"
@router.callback_query(F.data == "add_email")
async def add_email(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("✍️ Введите ваш email в формате example@gmail.com",
        reply_markup=cancel_profile_kb)
    await state.set_state(ProfileStates.waiting_for_email)
    await callback.answer()

# Обработка нажатия на "Добавить телефон"
@router.callback_query(F.data == "add_phone")
async def add_phone(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("✍️ Введите ваш номер телефона без пробелов и дополнительных знаков",
        reply_markup=cancel_profile_kb)
    await state.set_state(ProfileStates.waiting_for_phone)
    await callback.answer()


# Обработка ввода email
@router.message(ProfileStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    if not EMAIL_REGEX.match(email):
        await message.answer("🫢 Введите корректный email. Пример: `example@mail.com`",
            parse_mode="Markdown",
            reply_markup=cancel_profile_kb)
        return

    update_user_email(message.from_user.id, email)
    await message.answer("✅ Email сохранён",
        reply_markup=cancel_profile_kb)
    await state.clear()

# Обработка ввода телефона
@router.message(ProfileStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = re.sub(r"\D", "", message.text)

    PHONE_REGEX = re.compile(r"\d{10,15}$")
    
    if not PHONE_REGEX.match(phone):
        await message.answer("🫢 Введите корректный номер телефона (от 10 до 15 цифр).",
            reply_markup=cancel_profile_kb)
        return

    update_user_phone(message.from_user.id, phone)
    await message.answer("✅ Телефон сохранён",
        reply_markup=cancel_profile_kb)
    await state.clear()