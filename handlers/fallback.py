from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def handle_unknown_message(message: Message):
    await message.answer(f'''
🤷‍♂️Я не знаю такой команды(
Пожалуйста, воспользуйтесь кнопками меню 👇''')
