import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

# --- НАСТРОЙКИ ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_USERNAME = "@kospium"  # Сюда приходят заявки
PHONE_NUMBER = "+7 (XXX) XXX-XX-XX"  # Впишите свой номер для оплаты

# --- ОПИСАНИЯ УСЛУГ ---
INFO_LFC = "ЛФК — это индивидуально подобранные упражнения для решения задач здоровья и качества жизни."
INFO_MASSAGE = "Массаж по индивидуальной потребности: расслабляющий, коррекция фигуры (антицеллюлитный, лимфодренажный), спортивный. Зоны массажа подбираются под ваши цели."
INFO_NUTRITION = "Индивидуальный план питания на 1 месяц.\n\nЧтобы получить план, заполните анкету питания. После заполнения мы свяжемся с вами для уточнения деталей и оплаты."

# --- КЛАВИАТУРЫ ---
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Услуги", callback_data="services")],
        [InlineKeyboardButton("Цены", callback_data="prices")],
        [InlineKeyboardButton("Питание", callback_data="nutrition_info")],
        [InlineKeyboardButton("Записаться", callback_data="booking")],
        [InlineKeyboardButton("🎁 Сделать подарок", callback_data="gift")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_services_menu():
    keyboard = [
        [InlineKeyboardButton("ЛФК", callback_data="info_lfc")],
        [InlineKeyboardButton("Массаж", callback_data="info_massage")],
        [InlineKeyboardButton("Пакет ЛФК + Массаж (-10%) + Питание", callback_data="info_package")],
        [InlineKeyboardButton("Пробное занятие ЛФК + Массаж", callback_data="info_trial")],
        [InlineKeyboardButton("⬅ Назад в меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_booking_menu():
    keyboard = [
        [InlineKeyboardButton("ЛФК", callback_data="book_lfc")],
        [InlineKeyboardButton("Массаж", callback_data="book_massage")],
        [InlineKeyboardButton("Пакет ЛФК + Массаж + Питание", callback_data="book_package")],
        [InlineKeyboardButton("Пробное занятие", callback_data="book_trial")],
        [InlineKeyboardButton("⬅ Назад в меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_nutrition_menu():
    keyboard = [
        [InlineKeyboardButton("Заполнить анкету", callback_data="fill_anketa")],
        [InlineKeyboardButton("⬅ Назад в меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- КОМАНДЫ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в оздоровительный центр!\nВыберите действие:",
        reply_markup=get_main_menu()
    )

# --- ОБРАБОТЧИК КНОПОК ---
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "services":
        await query.edit_message_text(
            "Выберите услугу, чтобы узнать подробнее:",
            reply_markup=get_services_menu()
        )
        
    elif query.data == "prices":
        text = (
            "💰 Наши цены:\n\n"
            "• ЛФК (45-60 мин): 2000 руб.\n"
            "• Массаж (60 мин): 3000 руб.\n"
            "• Пакет ЛФК + Массаж + Питание (месяц): 32 400 руб. (-10%)\n"
            "• Пробное занятие ЛФК + Массаж + тестирование: 5000 руб."
        )
        await query.edit_message_text(text, reply_markup=get_main_menu())
        
    elif query.data == "booking":
        await query.edit_message_text(
            "Выберите услугу для записи:",
            reply_markup=get_booking_menu()
        )
        
    # --- ИНФОРМАЦИЯ ОБ УСЛУГАХ (Цена и время вверху) ---
    elif query.data == "info_lfc":
        text = (
            "🏋️ ЛФК (45-60 мин)\n"
            "💰 Цена: 2000 руб.\n\n"
            f"{INFO_LFC}"
        )
        await query.edit_message_text(text, reply_markup=get_services_menu())
        
    elif query.data == "info_massage":
        text = (
            "💆 Массаж (60 мин)\n"
            "💰 Цена: 3000 руб.\n\n"
            f"{INFO_MASSAGE}"
        )
        await query.edit_message_text(text, reply_markup=get_services_menu())
        
    elif query.data == "info_package":
        text = (
            "📦 Пакет ЛФК + Массаж + Питание (месяц)\n"
            "💰 Цена: 32 400 руб. (-10%)\n"
            "⏱ Состав: 12 занятий ЛФК + 4 массажа + план питания.\n\n"
            "Отличный вариант для комплексного подхода к здоровью!"
        )
        await query.edit_message_text(text, reply_markup=get_services_menu())
        
    elif query.data == "info_trial":
        text = (
            "🎯 Пробное занятие ЛФК + Массаж + тестирование\n"
            "💰 Цена: 5000 руб.\n\n"
            "Отличная возможность познакомиться с нашим подходом и понять, подходит ли он вам."
        )
        await query.edit_message_text(text, reply_markup=get_services_menu())

    # --- ПИТАНИЕ ---
    elif query.data == "nutrition_info":
        await query.edit_message_text(
            INFO_NUTRITION,
            reply_markup=get_nutrition_menu()
        )

    elif query.data == "fill_anketa":
        await query.edit_message_text(
            "📝 Анкета питания\n\n"
            "Пожалуйста, ответьте на следующие вопросы одним сообщением:\n\n"
            "1. Ваш возраст, рост, вес.\n"
            "2. Цель (похудеть, набрать массу, поддерживать).\n"
            "3. Есть ли аллергии или непереносимость продуктов?\n"
            "4. Сколько раз в день вы едите?\n"
            "5. Ваш уровень активности (сидячий, средний, высокий).\n"
            "6. Что вы обычно едите на завтрак, обед и ужин?\n\n"
            "Напишите все ответы одним сообщением."
        )
        context.user_data["waiting_anketa"] = True

    # --- ПОДАРОК ---
    elif query.data == "gift":
        await query.edit_message_text(
            "🎁 Вы хотите сделать подарок!\n\n"
            "Напишите, пожалуйста, информацию в таком формате (одним сообщением):\n\n"
            "1. Имя получателя\n"
            "2. Телефон получателя\n"
            "3. Адрес, где делать услугу\n"
            "4. Дополнительная информация (пожелания, нюансы)"
        )
        context.user_data["waiting_gift"] = True

    # --- ЗАПИСЬ НА УСЛУГУ ---
    elif query.data.startswith("book_"):
        service_key = query.data.replace("book_", "")
        context.user_data["service"] = service_key
        
        service_names = {
            "lfc": "ЛФК",
            "massage": "Массаж",
            "package": "Пакет ЛФК + Массаж + Питание",
            "trial": "Пробное занятие ЛФК + Массаж"
        }
        service_name = service_names.get(service_key, "Услуга")
        
        await query.edit_message_text(
            f"Вы выбрали: {service_name}\n\n"
            "Напишите ваши данные одним сообщением в таком формате:\n\n"
            "1. Ваше имя\n"
            "2. Ваш телефон\n"
            "3. Адрес, где нужно провести услугу\n"
            "4. Удобный день и время"
        )
        
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            "Главное меню:",
            reply_markup=get_main_menu()
        )

# --- ОБРАБОТЧИК ТЕКСТА ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_name = update.effective_user.first_name
    user_username = update.effective_user.username or "нет username"
    
    # 1. Анкета питания
    if user_data.get("waiting_anketa"):
        user_data["waiting_anketa"] = False
        anketa_text = update.message.text
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_USERNAME,
                text=f"🥗 НОВАЯ АНКЕТА ПИТАНИЯ!\n\n"
                     f"От: {user_name} (@{user_username})\n\n"
                     f"Ответы:\n{anketa_text}"
            )
            await update.message.reply_text(
                "✅ Спасибо! Ваша анкета принята.\n\n"
                "ℹ️ Информация в обработке. Обычно это занимает 1-2 дня.\n\n"
                f"💳 Для оплаты переведите сумму на номер:\n"
                f"{PHONE_NUMBER} (Сбербанк)\n\n"
                "🔗 Ссылка на оплату: (в разработке)",
                reply_markup=get_main_menu()
            )
        except Exception:
            await update.message.reply_text("Ошибка. Напишите нам: @kospium")
        return

    # 2. Подарок
    if user_data.get("waiting_gift"):
        user_data["waiting_gift"] = False
        gift_text = update.message.text
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_USERNAME,
                text=f"🎁 НОВЫЙ ПОДАРОК!\n\n"
                     f"От: {user_name} (@{user_username})\n\n"
                     f"Данные получателя:\n{gift_text}"
            )
            await update.message.reply_text(
                "✅ Спасибо! Информация о подарке принята.\n"
                "Мы свяжемся с вами для уточнения деталей оплаты.",
                reply_markup=get_main_menu()
            )
        except Exception:
            await update.message.reply_text("Ошибка. Напишите нам: @kospium")
        return

    # 3. Запись на услугу
    if "service" in user_data and "details" not in user_data:
        user_data["details"] = update.message.text
        
        service_names = {
            "lfc": "ЛФК",
            "massage": "Массаж",
            "package": "Пакет ЛФК + Массаж + Питание",
            "trial": "Пробное занятие ЛФК + Массаж"
        }
        service_name = service_names.get(user_data["service"], "Услуга")
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_USERNAME,
                text=f"🔔 НОВАЯ ЗАЯВКА!\n\n"
                     f"Услуга: {service_name}\n\n"
                     f"Данные клиента:\n{user_data['details']}\n\n"
                     f"Telegram: @{user_username}"
            )
            await update.message.reply_text(
                f"Спасибо, {user_name}! Ваша заявка принята.\n"
                "Мы свяжемся с вами для подтверждения.",
                reply_markup=get_main_menu()
            )
        except Exception:
            await update.message.reply_text("Ошибка. Напишите нам: @kospium")
        
        user_data.clear()

# --- ЗАПУСК ---
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Бот запускается...")
    application.run_polling()
