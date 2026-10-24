import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# 1. Получаем токен из переменных окружения (на Render он будет там)
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# 2. Функция для создания кнопок меню
def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Услуги", callback_data="services")],
        [InlineKeyboardButton("Цены", callback_data="prices")],
        [InlineKeyboardButton("Записаться", callback_data="booking")]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. Команда /start - показывает приветствие и меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в массажный салон!\nВыберите действие:",
        reply_markup=get_menu_keyboard()
    )

# 4. Обработчик нажатий на кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        await query.edit_message_text("У нас есть: Классический массаж, Спортивный массаж")
    elif query.data == "prices":
        await query.edit_message_text("Классический: 2000 руб.\nСпортивный: 2500 руб.")
    elif query.data == "booking":
        await query.edit_message_text("Функция записи в разработке. Скоро здесь можно будет выбрать время!")

# 5. Запуск бота
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))
    print("Бот запускается...")
    application.run_polling()
