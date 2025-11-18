Саян, [18.11.2025 19:33]
import os
import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

# Настройки
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Очистка webhook перед запуском
async def clear_webhook():
    """Очищаем webhook перед запуском polling"""
    try:
        import requests
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
        logger.info(f"Webhook очищен: {response.json()}")
    except Exception as e:
        logger.error(f"Ошибка при очистке webhook: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        logger.info(f"Пользователь {user.id} ({user.first_name}) запустил бота")
        
        # Создаем клавиатуру с девушками
        keyboard = [
            [KeyboardButton("🌙 Луна"), KeyboardButton("🔥 Стелла")],
            [KeyboardButton("🎌 Сакура"), KeyboardButton("👑 Виктория")],
            [KeyboardButton("🐍 Клео"), KeyboardButton("🏃‍♀️ Ники")],
            [KeyboardButton("💃 Жасмин"), KeyboardButton("🖤 Рокси")],
            [KeyboardButton("📊 Статус"), KeyboardButton("🔄 Сброс")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_text = """
🌟 *Добро пожаловать в AI Girls Bot!* 🌟

Выбери девушку для общения:

🌙 *Луна* - Нежная романтичная мечтательница
🔥 *Стелла* - Сексуальная и уверенная соблазнительница  
🎌 *Сакура* - Милая аниме девушка-куноичи
👑 *Виктория* - Элегантная аристократка
🐍 *Клео* - Загадочная египтянка
🏃‍♀️ *Ники* - Спортивная и энергичная
💃 *Жасмин* - Чувственная восточная красавица
🖤 *Рокси* - Дерзкая бунтарка

Нажми на кнопку с именем девушки чтобы начать общение!
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка в команде start: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуй еще раз.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений"""
    try:
        user_message = update.message.text
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        logger.info(f"Сообщение от {user_id} ({user_name}): {user_message}")
        
        # Показываем что бот печатает
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Простые ответы на кнопки
        if user_message == "📊 Статус":
            status_text = f"""
📊 *Статус бота:*

✅ Бот работает нормально
👤 Пользователь: {user_name}
🆔 ID: {user_id}
💬 Сообщение: {user_message}

Выбери девушку для начала общения! 💫
            """
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        elif user_message == "🔄 Сброс":
            await update.message.reply_text("🔄 Прогресс сброшен! Выбери девушку заново.")
            
        elif user_message in ["🌙 Луна", "🔥 Стелла", "🎌 Сакура", "👑 Виктория", 
                            "🐍 Клео", "🏃‍♀️ Ники", "💃 Жасмин", "🖤 Рокси"]:
            girl_name = user_message.split()[1]  # Берем только имя
            responses = {
                "Луна": [
                    "Привет! Я Луна 🌙\nРада познакомиться! Я люблю романтические вечера и мечтать о звездах...",
                    "О, ты выбрал меня! Я Луна 🌙\nДавай поговорим о чем-нибудь прекрасном?"
                ],
                "Стелла": [
                    "Привет, я Стелла 🔥\nТы выглядишь... интересно. Что привело тебя ко мне?",
                    "О, наконец-то! Я Стелла 🔥\nГотова к страстному приключению?"

Саян, [18.11.2025 19:33]
],
                "Сакура": [
                    "Конничива! Я Сакура 🎌\nРада встрече! Ты такой милый!",
                    "Я Сакура 🎌\nЛюблю аниме и сакуру! А ты что любишь?"
                ],
                "Виктория": [
                    "Здравствуйте. Я Виктория 👑\nНадеюсь, вы соблюдаете приличия.",
                    "Я Виктория 👑\nПриятно видеть человека с хорошими манерами."
                ],
                "Клео": [
                    "Приветствую. Я Клео 🐍\nТы готов разгадать мои тайны?",
                    "Я Клео 🐍\nДревние боги шепчут мне твое имя..."
                ],
                "Ники": [
                    "Йоу! Я Ники 🏃‍♀️\nДавай двигаться! Что планируешь?",
                    "Привет! Я Ники 🏃‍♀️\nГотова к активностям! А ты?"
                ],
                "Жасмин": [
                    "Ассаламу алейкум... Я Жасмин 💃\nПозволь мне увлечь тебя в танец...",
                    "Я Жасмин 💃\nМои танцы расскажут тебе историю любви..."
                ],
                "Рокси": [
                    "Хэй. Я Рокси 🖤\nНе ожидал такой крутой девчонки, да?",
                    "Рокси 🖤 на связи.\nНадеюсь, ты не из скучных..."
                ]
            }
            
            import random
            response = random.choice(responses.get(girl_name, ["Привет! Рада познакомиться! 💫"]))
            await update.message.reply_text(response)
            
        else:
            # Общий ответ на любое сообщение
            responses = [
                "Интересно... расскажи мне больше! 💫",
                "Хм, никогда об этом не думала... а что ты сам думаешь? 🤔",
                "Спасибо, что делишься этим со мной! 💖",
                "Продолжай, мне нравится слушать тебя! ✨",
                "Давай поговорим о чем-то другом? Выбери девушку из меню! 👆"
            ]
            import random
            response = random.choice(responses)
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Ошибка в handle_message: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке сообщения.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка при обработке обновления: {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка. Попробуй еще раз или используй /start"
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение об ошибке: {e}")

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
        
        # Очищаем webhook и запускаем polling
        async def post_init(application):
            await application.bot.delete_webhook()
            logger.info("✅ Webhook очищен, запускаем polling...")
        
        application = Application.builder().token(TOKEN).post_init(post_init).build()
        
        # Пересоздаем обработчики после пересборки application
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("🤖 Запускаю бота...")
        
        # Запускаем бота с очисткой старых обновлений
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.

Саян, [18.11.2025 19:33]
error(f"❌ Критическая ошибка при запуске бота: {e}")

if name == "__main__":
    # Очищаем webhook синхронно перед запуском
    try:
        import requests
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
        logger.info(f"Webhook очищен перед запуском: {response.json()}")
    except Exception as e:
        logger.error(f"Ошибка при предварительной очистке webhook: {e}")
    
    main()
