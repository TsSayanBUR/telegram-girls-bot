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
        "Привет! Я Луна. Рада познакомиться!",
        "О, ты выбрал меня! Я Луна. Давай поговорим?",
        "Здравствуй! Я Луна. Люблю романтические вечера."
    ],
    "stella": [
        "Привет, я Стелла. Ты выглядишь интересно!",
        "О, наконец-то! Я Стелла. Готова к приключениям?",
        "Я Стелла. Что привело тебя ко мне?"
    ],
    "sakura": [
        "Конничива! Я Сакура. Рада встрече!",
        "Я Сакура. Люблю аниме и сакуру!",
        "Сакура на связи! Ты такой милый!"
    ],
    "victoria": [
        "Здравствуйте. Я Виктория. Надеюсь, вы соблюдаете приличия.",
        "Я Виктория. Приятно видеть человека с манерами.",
        "Виктория к вашим услугам."
    ],
    "cleo": [
        "Приветствую. Я Клео. Ты готов разгадать мои тайны?",
        "Я Клео. Древние боги шепчут мне твое имя.",
        "Клео приветствует тебя, смертный."
    ],
    "niki": [
        "Йоу! Я Ники. Давай двигаться!",
        "Привет! Я Ники. Готова к активностям!",
        "Ники на связи! Что планируешь?"
    ],
    "jasmin": [
        "Ассаламу алейкум. Я Жасмин. Позволь мне увлечь тебя.",
        "Я Жасмин. Мои танцы расскажут историю любви.",
        "Жасмин приветствует тебя."
    ],
    "roxy": [
        "Хэй. Я Рокси. Не ожидал такой крутой девчонки, да?",
        "Рокси на связи. Надеюсь, ты не из скучных.",
        "Я Рокси. Что смотришь? Давай общаться!"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
            [KeyboardButton("🌙 Луна"), KeyboardButton("🔥 Стелла")],
            [KeyboardButton("🎌 Сакура"), KeyboardButton("👑 Виктория")],
            [KeyboardButton("🐍 Клео"), KeyboardButton("🏃‍♀️ Ники")],
            [KeyboardButton("💃 Жасмин"), KeyboardButton("🖤 Рокси")],
            [KeyboardButton("📊 Статус бота")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_text = "🌟 Добро пожаловать в AI Girls Bot! 🌟\n\nВыбери девушку для общения:\n\n🌙 Луна - Нежная романтичная\n🔥 Стелла - Сексуальная и уверенная\n🎌 Сакура - Милая аниме девушка\n👑 Виктория - Элегантная аристократка\n🐍 Клео - Загадочная египтянка\n🏃‍♀️ Ники - Спортивная и энергичная\n💃 Жасмин - Чувственная восточная\n🖤 Рокси - Дерзкая бунтарка\n\nНажми на кнопку чтобы начать общение!"
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info("Пользователь запустил бота")
        
    except Exception as e:
        logger.error("Ошибка в start: " + str(e))
        await update.message.reply_text("Произошла ошибка. Попробуй еще раз.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        user_id = update.effective_user.id
        
        logger.info("Сообщение от пользователя: " + user_message)
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        if user_message == "📊 Статус бота":
            status_text = "📊 Статус бота:\n\n✅ Бот работает нормально\n👤 Пользователь ID: " + str(user_id) + "\n🚀 Хостинг: Render.com\n💬 Получил сообщение\n\nВыбери девушку для общения! 💫"
            await update.message.reply_text(status_text)
            
        elif user_message == "🌙 Луна":
            response = random.choice(GIRL_RESPONSES["luna"])
            await update.message.reply_text(response)
            
        elif user_message == "🔥 Стелла":
            response = random.choice(GIRL_RESPONSES["stella"])
            await update.message.

reply_text(response)
            
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
            responses = [
                "Интересно... расскажи мне больше!",
                "Хм, а что ты сам думаешь об этом?",
                "Спасибо, что делишься со мной!",
                "Продолжай, мне нравится слушать тебя!",
                "Давай поговорим о чем-то другом? Выбери девушку из меню!"
            ]
            response = random.choice(responses)
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error("Ошибка в handle_message: " + str(e))
        await update.message.reply_text("Произошла ошибка при обработке сообщения.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке обновления: " + str(context.error))

def main():
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN не найден в переменных окружения!")
        return
    
    try:
        application = Application.builder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("Запускаю бота...")
        
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error("Критическая ошибка при запуске бота: " + str(e))

if name == "__main__":
    main()
