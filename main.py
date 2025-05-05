import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


load_dotenv
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Приветствие с подставленным именем пользователя
    welcome_text = f'''Привет, {update.effective_user.first_name}!
Я бот, который поможет тебе купить подписку на телеграм-канал 'Common Data'.
Чтобы узнать подробности, напиши /subscribe или нажми на кнопку ниже.'''

    # Кнопка "Купить подписку"
    keyboard = [
        [InlineKeyboardButton("Купить подписку", callback_data='subscribe')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

if __name__ == '__main__':
    # Создаем объект приложения и настраиваем токен
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))
    
    print("Бот запущен...")
    app.run_polling()
