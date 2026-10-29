import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_USERNAME = "@kospium"  # Сюда будут приходить заявки

# --- УСЛУГИ И ЦЕНЫ ---
SERVICES = {
    "lfc": {"name": "ЛФК", "price": "2000 руб.", "duration": "45-60 мин"},
    "massage": {"name": "Массаж", "price": "3000 руб.", "duration": "60 мин"},
    "package": {"name": "Пакет ЛФК + Массаж (месяц)", "price": "32 400 руб. (-10%)", "duration": "12 ЛФК + 4 массажа"}
}

# --- Клавиатуры ---
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Услуги", callback_data="services")],
        [InlineKeyboardButton("Цены", callback_data="prices")],
        [InlineKeyboardButton("Записаться", callback_data="booking")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_services_menu():
    keyboard = [
        [InlineKeyboardButton("ЛФК", callback_data="book_lfc")],
        [InlineKeyboardButton("Массаж", callback_data="book_massage")],
        [InlineKeyboardButton("Пакет ЛФК + Массаж", callback_data="book_package")],
        [InlineKeyboardButton("⬅ Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в оздоровительный центр!\nВыберите действие:",
        reply_markup=get_main_menu()
    )

# --- Обработчик кнопок ---
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "services":
        text = "Наши услуги:\n\n"
        for key, info in SERVICES.items():
            text += f"• {info['name']} — {info['price']} ({info['duration']})\n"
        await query.edit_message_text(text, reply_markup=get_main_menu())
        
    elif query.data == "prices":
        text = "Цены:\n\n"
        for key, info in SERVICES.items():
            text += f"• {info['name']}: {info['price']}\n"
        await query.edit_message_text(text, reply_markup=get_main_menu())
        
    elif query.data == "booking":
        await query.edit_message_text(
            "Выберите услугу для записи:",
            reply_markup=get_services_menu()
        )
        
    elif query.data.startswith("book_"):
        service_key = query.data.replace("book_", "")
        context.user_data["service"] = service_key
        service_name = SERVICES[service_key]["name"]
        await query.edit_message_text(
            f"Вы выбрали: {service_name}\n\nНапишите удобный день и время (например: 'Завтра в 15:00' или 'В субботу утром'):"
        )
        
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            "Главное меню:",
            reply_markup=get_main_menu()
        )

# --- Обработчик текстовых сообщений (время и имя) ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    
    # Если пользователь в процессе записи (выбрал услугу, но не ввел время)
    if "service" in user_data and "time" not in user_data:
        user_data["time"] = update.message.text
        await update.message.reply_text("Напишите ваше имя:")
    
    # Если пользователь ввел время, но не ввел имя
    elif "service" in user_data and "time" in user_data and "name" not in user_data:
        user_data["name"] = update.message.text
        user_data["user_id"] = update.effective_user.id
        user_data["username"] = update.effective_user.username or "нет username"
        
        service_name = SERVICES[user_data["service"]]["name"]
        
        # Отправляем заявку вам
        try:
            await context.bot.send_message(
                chat_id=ADMIN_USERNAME,
                text=f"🔔 НОВАЯ ЗАЯВКА!\n\n"
                     f"Услуга: {service_name}\n"
                     f"Время: {user_data['time']}\n"
                     f"Имя: {user_data['name']}\n"
                     f"Telegram: @{user_data['username']}"
            )
            await update.message.reply_text(
                f"Спасибо, {user_data['name']}! Ваша заявка принята.\nМы свяжемся с вами для подтверждения.",
                reply_markup=get_main_menu()
            )
        except Exception as e:
            await update.message.reply_text(
                "Произошла ошибка при отправке заявки. Пожалуйста, напишите нам напрямую: @kospium"
            )
        
        # Очищаем данные пользователя после записи
        user_data.clear()

# --- Запуск ---
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Бот запускается...")
    application.run_polling()
