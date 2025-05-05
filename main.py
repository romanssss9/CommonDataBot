import os
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, LabeledPrice
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, ConversationHandler, MessageHandler, filters,
    PreCheckoutQueryHandler
)

from database import (
    init_db, add_or_update_user, update_user_email,
    update_user_phone, get_user, update_user_subscription
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

EMAIL, PHONE = range(2)

# Главное меню клавиатура
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("📋 Меню"), KeyboardButton("💳 Купить подписку")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_or_update_user(user.id, user.first_name, user.username)
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Я бот, который поможет тебе купить подписку на телеграм-канал Common Data.\n"
        "Нажми 📋 Меню, чтобы начать.",
        reply_markup=get_main_keyboard()
    )


# Меню
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Добавить email", callback_data='add_email')],
        [InlineKeyboardButton("Добавить телефон", callback_data='add_phone')],
        [InlineKeyboardButton("Показать профиль", callback_data='show_profile')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)


# Кнопки меню
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'add_email':
        await query.message.reply_text("Введите ваш email:")
        return EMAIL
    elif query.data == 'add_phone':
        await query.message.reply_text("Введите ваш телефон:")
        return PHONE
    elif query.data == 'show_profile':
        user_data = get_user(query.from_user.id)
        if user_data:
            msg = (
                f"👤 Имя: {user_data['first_name']}\n"
                f"🆔 Telegram ID: {user_data['telegram_id']}\n"
                f"📧 Email: {user_data['email'] or 'не указан'}\n"
                f"📱 Телефон: {user_data['phone'] or 'не указан'}\n"
                f"💼 Подписка активна: {'Да' if user_data['is_subscription'] else 'Нет'}"
            )
        else:
            msg = "Профиль не найден в базе."
        await query.message.reply_text(msg)
        return ConversationHandler.END


# Покупка подписки
async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = [LabeledPrice("Подписка на 1 месяц", 29900)]  # Цена в копейках

    await context.bot.send_invoice(
        chat_id=update.effective_user.id,
        title="Подписка на Common Data",
        description="Доступ к закрытому каналу и сообществу.",
        payload="common-data-subscription",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="subscribe",
    )


# Подтверждение перед оплатой
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != 'common-data-subscription':
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        await query.answer(ok=True)


# Успешная оплата
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Оплата прошла успешно! Подписка активирована.")
    update_user_subscription(update.effective_user.id, True)


# Email
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    update_user_email(update.effective_user.id, email)
    await update.message.reply_text("Email сохранён ✅")
    return ConversationHandler.END


# Телефон
async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    update_user_phone(update.effective_user.id, phone)
    await update.message.reply_text("Телефон сохранён ✅")
    return ConversationHandler.END


# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END


# Запуск
if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))

    # Кнопки главного меню
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📋 Меню$"), menu))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^💳 Купить подписку$"), buy_subscription))

    # Оплата
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Inline кнопки и email/телефон
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()
