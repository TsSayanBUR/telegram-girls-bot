import os
import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🌙 Луна"), KeyboardButton("🔥 Стелла")],
        [KeyboardButton("📊 Статус")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    text = "Привет! Я бот с девушками. Выбери действие:"
    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    if user_message == "🌙 Луна":
        responses = [
            "Привет! Я Луна. Рада познакомиться!",
            "Здравствуй! Я Луна. Как твои дела?",
            "О, ты выбрал меня! Я Луна."
        ]
        response = random.choice(responses)
        await update.message.reply_text(response)
        
    elif user_message == "🔥 Стелла":
        responses = [
            "Привет, я Стелла. Ты выглядишь интересно!",
            "Я Стелла. Что привело тебя ко мне?",
            "О, наконец-то! Я Стелла."
        ]
        response = random.choice(responses)
        await update.message.reply_text(response)
        
    elif user_message == "📊 Статус":
        await update.message.reply_text("✅ Бот работает отлично!")
        
    else:
        await update.message.reply_text("Выбери действие из меню!")

def main():
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not found")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()


