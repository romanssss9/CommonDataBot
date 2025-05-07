from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from keyboards import main_kb, start_kb
from database import add_or_update_user, init_db

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    init_db()
    user = message.from_user
    add_or_update_user(user.id, user.first_name, user.username)

    await message.answer(
        f'''
👋 Привет, {user.first_name}!
Я бот, который поможет тебе купить подписку на телеграм канал Common Data!
Здесь ты найдешь много эксклюзивного контента и полезных материалов по трудоустройству и работе в IT 💻''',
        reply_markup=main_kb    
    )

    await message.answer(
        f'''
💪 Выбирай тариф и добро пожаловать в лучшее место для твоего карьерного роста''',
        reply_markup=start_kb
    )