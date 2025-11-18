import os
import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Простые ответы для девушек
GIRL_RESPONSES = {
    "luna": [
        "Привет! Я Луна 🌙 Рада познакомиться!",
        "О, ты выбрал меня! Я Луна 🌙 Давай поговорим?",
        "Здравствуй! Я Луна 🌙 Люблю романтические вечера..."
    ],
    "stella": [
        "Привет, я Стелла 🔥 Ты выглядишь интересно!",
        "О, наконец-то! Я Стелла 🔥 Готова к приключениям?",
        "Я Стелла 🔥 Что привело тебя ко мне?"
    ],
    "sakura": [
        "Конничива! Я Сакура 🎌 Рада встрече!",
        "Я Сакура 🎌 Люблю аниме и сакуру!",
        "Сакура 🎌 на связи! Ты такой милый!"
    ],
    "victoria": [
        "Здравствуйте. Я Виктория 👑 Надеюсь, вы соблюдаете приличия.",
        "Я Виктория 👑 Приятно видеть человека с манерами.",
        "Виктория 👑 к вашим услугам."
    ],
    "cleo": [
        "Приветствую. Я Клео 🐍 Ты готов разгадать мои тайны?",
        "Я Клео 🐍 Древние боги шепчут мне твое имя...",
        "Клео 🐍 приветствует тебя, смертный."
    ],
    "niki": [
        "Йоу! Я Ники 🏃‍♀️ Давай двигаться!",
        "Привет! Я Ники 🏃‍♀️ Готова к активностям!",
        "Ники 🏃‍♀️ на связи! Что планируешь?"
    ],
    "jasmin": [
        "Ассаламу алейкум... Я Жасмин 💃 Позволь мне увлечь тебя...",
        "Я Жасмин 💃 Мои танцы расскажут историю любви...",
        "Жасмин 💃 приветствует тебя..."
    ],
    "roxy": [
        "Хэй. Я Рокси 🖤 Не ожидал такой крутой девчонки, да?",
        "Рокси 🖤 на связи. Надеюсь, ты не из скучных...",
        "Я Рокси 🖤 Что смотришь? Давай общаться!"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        keyboard = [
            [KeyboardButton("🌙 Луна"), KeyboardButton("🔥 Стелла")],
            [KeyboardButton("🎌 Сакура"), KeyboardButton("👑 Виктория")],
            [KeyboardButton("🐍 Клео"), KeyboardButton("🏃‍♀️ Ники")],
            [KeyboardButton("💃 Жасмин"), KeyboardButton("🖤 Рокси")],
            [KeyboardButton("📊 Статус бота")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_text = """
🌟 *Добро пожаловать в AI Girls Bot!* 🌟

Выбери девушку для общения:

🌙 *Луна* - Нежная романтичная
🔥 *Стелла* - Сексуальная и уверенная  
🎌 *Сакура* - Милая аниме девушка
👑 *Виктория* - Элегантная аристократка
🐍 *Клео* - Загадочная египтянка
🏃‍♀️ *Ники* - Спортивная и энергичная
💃 *Жасмин* - Чувственная восточная
🖤 *Рокси* - Дерзкая бунтарка

Нажми на кнопку чтобы начать общение!
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"Пользователь {update.effective_user.id} запустил бота")
        
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуй еще раз.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений"""
    try:
        user_message = update.message.text
        user_id = update.effective_user.id
        
        logger.info(f"Сообщение от {user_id}: {user_message}")
        
        # Показываем что бот печатает
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Обработка кнопок
        if user_message == "📊 Статус бота":
            status_text = f"""
📊 *Статус бота:*

✅ Бот работает нормально
👤 Пользователь ID: {user_id}
🚀 Хостинг: Render.com
💬 Получил сообщение: "{user_message}"

Выбери девушку для общения! 💫
            """
            await update.message.
            reply_text(status_text, parse_mode='Markdown')
            
        elif user_message == "🌙 Луна":
            response = random.choice(GIRL_RESPONSES["luna"])
            await update.message.reply_text(response)
            
        elif user_message == "🔥 Стелла":
            response = random.choice(GIRL_RESPONSES["stella"])
            await update.message.reply_text(response)
            
        elif user_message == "🎌 Сакура":
            response = random.choice(GIRL_RESPONSES["sakura"])
            await update.message.reply_text(response)
            
        elif user_message == "👑 Виктория":
            response = random.choice(GIRL_RESPONSES["victoria"])
            await update.message.reply_text(response)
            
        elif user_message == "🐍 Клео":
            response = random.choice(GIRL_RESPONSES["cleo"])
            await update.message.reply_text(response)
            
        elif user_message == "🏃‍♀️ Ники":
            response = random.choice(GIRL_RESPONSES["niki"])
            await update.message.reply_text(response)
            
        elif user_message == "💃 Жасмин":
            response = random.choice(GIRL_RESPONSES["jasmin"])
            await update.message.reply_text(response)
            
        elif user_message == "🖤 Рокси":
            response = random.choice(GIRL_RESPONSES["roxy"])
            await update.message.reply_text(response)
            
        else:
            # Общий ответ на любое сообщение
            responses = [
                "Интересно... расскажи мне больше! 💫",
                "Хм, а что ты сам думаешь об этом? 🤔",
                "Спасибо, что делишься со мной! 💖",
                "Продолжай, мне нравится слушать тебя! ✨",
                "Давай поговорим о чем-то другом? Выбери девушку из меню! 👆"
            ]
            response = random.choice(responses)
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Ошибка в handle_message: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке сообщения.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка при обработке обновления: {context.error}")

def main():
    """Основная функция запуска бота"""
    if not TOKEN:
        logger.error("❌ TELEGRAM_TOKEN не найден в переменных окружения!")
        return
    
    try:
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("🤖 Запускаю бота...")
        
        # Запускаем бота
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка при запуске бота: {e}")

if name == "__main__":
    main()
