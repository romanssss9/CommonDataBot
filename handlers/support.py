from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import support_kb

router = Router()

@router.message(F.text == '🤝 Поддержка')
@router.message(Command('help'))
async def support(message: Message):
    await message.answer(f'''
Если у вас остались вопросы, вы всегда можете обратиться в поддержку 👇''',
    reply_markup=support_kb)