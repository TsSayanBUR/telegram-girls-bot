import os
import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Luna"), KeyboardButton("Stella")],
        [KeyboardButton("Status")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    text = "Hello! I am a bot with girls. Choose an action:"
    update.message.reply_text(text, reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    
    if user_message == "Luna":
        responses = [
            "Hello! I'm Luna. Nice to meet you!",
            "Hi! I'm Luna. How are you?",
            "Oh, you chose me! I'm Luna."
        ]
        response = random.choice(responses)
        update.message.reply_text(response)
        
    elif user_message == "Stella":
        responses = [
            "Hi, I'm Stella. You look interesting!",
            "I'm Stella. What brought you to me?",
            "Finally! I'm Stella."
        ]
        response = random.choice(responses)
        update.message.reply_text(response)
        
    elif user_message == "Status":
        update.message.reply_text("Bot is working fine!")
        
    else:
        update.message.reply_text("Please choose an action from the menu!")

def main():
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN not found")
        return
    
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    logger.info("Starting bot...")
    updater.start_polling()
    updater.idle()

if name == "__main__":
    main()



