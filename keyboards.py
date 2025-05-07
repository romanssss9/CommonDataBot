from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardButton, InlineKeyboardMarkup)
from config import SUPPORT_URL

buttons = {'profile': '🙋‍♂️ Профиль',
           'my_subscrition': '🗂️ Моя подписка',
           'buy_subscrition': '💳 Купить подписку',
           'support': '🤝 Поддержка'}

main_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=buttons['buy_subscrition']), KeyboardButton(text=buttons['my_subscrition'])],
        [KeyboardButton(text=buttons['profile']), KeyboardButton(text=buttons['support'])]
    ],
        resize_keyboard=True
    )

profile_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📧 Добавить email", callback_data="add_email")],
            [InlineKeyboardButton(text="📱 Добавить телефон", callback_data="add_phone")]
        ]
    )

start_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Смотреть тарифы", callback_data="buy_subscrition")]
        ]
    )

support_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Написать в поддержку", url=SUPPORT_URL)]
        ]
    )

cancel_profile_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🙋‍♂️ В профиль", callback_data="show_profile")]
        ]
    )
