from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import buttons,  profile_kb
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

# Обработка команды "Профиль" (кнопка Профиль из главного меню)
@router.message(F.text == buttons['profile'])
async def show_profile(message: Message):

    # Получаем данные пользователя из базы
    user_data = get_user(message.from_user.id)
    
    if user_data:
        msg = (
            f"👤 Имя: {user_data['first_name']}\n"
            f"🆔 Telegram ID: {user_data['telegram_id']}\n"
            f"📧 Email: {user_data['email'] or 'не указан'}\n"
            f"📱 Телефон: {user_data['phone'] or 'не указан'}\n"
            f"💼 Подписка активна: {'Да' if user_data['is_subscription'] else 'Нет'}"
        )
    else:
        msg = "Профиль не найден."

    # Отправляем информацию о пользователе
    await message.answer(msg, reply_markup=profile_kb)

    
# Обработка нажатия на "Добавить email"
@router.callback_query(F.data == "add_email")
async def add_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваш email в формате example@gmail.com:")
    await state.set_state(ProfileStates.waiting_for_email)
    await callback.answer()

# Обработка нажатия на "Добавить телефон"
@router.callback_query(F.data == "add_phone")
async def add_phone(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваш номер телефона:")
    await state.set_state(ProfileStates.waiting_for_phone)
    await callback.answer()


# Обработка ввода email
@router.message(ProfileStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()

    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    if not EMAIL_REGEX.match(email):
        await message.answer("⚠️ Пожалуйста, введите корректный email. Пример: `example@mail.com`", parse_mode="Markdown")
        return

    update_user_email(message.from_user.id, email)
    await message.answer("✅ Email сохранён.")
    await state.clear()

# Обработка ввода телефона
@router.message(ProfileStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip().replace(" ", "")

    PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")
    
    if not PHONE_REGEX.match(phone):
        await message.answer("⚠️ Введите корректный номер телефона (от 10 до 15 цифр, можно с `+` в начале).")
        return

    update_user_phone(message.from_user.id, phone)
    await message.answer("✅ Телефон сохранён.")
    await state.clear()
