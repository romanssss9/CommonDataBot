from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import support_kb

router = Router()

@router.message(F.text == '🤝 Поддержка')
async def support(message: Message):
    await message.answer(f'''
Если у вас остались вопросы, вы всегда можете обратиться в поддержку 👇''',
    reply_markup=support_kb)