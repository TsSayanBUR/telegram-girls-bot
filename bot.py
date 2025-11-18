import logging
import random
import re
import requests
import json
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
import datetime
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройки
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8286246486:AAEAYZcReAcrvDSd2Nr5cfIuCbXan_rLDVA')
HF_TOKEN = os.getenv('HF_TOKEN')  # Токен Hugging Face (опционально)
DATA_FILE = "user_data.json"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class AIService:
    def __init__(self):
        self.hf_token = HF_TOKEN
        self.ai_enabled = bool(HF_TOKEN)
    
    async def generate_image(self, prompt, girl_name):
        """Генерация изображения через Hugging Face"""
        if not self.ai_enabled:
            return None
            
        try:
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            
            # Улучшаем промпт в зависимости от девушки
            enhanced_prompt = self._enhance_prompt(prompt, girl_name)
            
            response = requests.post(
                API_URL, 
                headers=headers, 
                json={"inputs": enhanced_prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                return response.content
            else:
                logging.error(f"Ошибка генерации изображения: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Ошибка в generate_image: {e}")
            return None
    
    def _enhance_prompt(self, prompt, girl_name):
        """Улучшаем промпт для генерации изображений"""
        style_prompts = {
            "luna": "beautiful anime girl with silver hair, romantic setting, moon, fantasy art, detailed face",
            "stella": "sexy beautiful woman, seductive pose, realistic photo, perfect body, bedroom setting",
            "sakura": "cute anime girl, japanese style, cherry blossoms, kawaii, pink hair, school uniform",
            "victoria": "elegant aristocratic woman, victorian dress, palace interior, sophisticated beauty",
            "cleo": "mysterious egyptian queen, golden jewelry, desert background, hieroglyphs, exotic beauty",
            "niki": "athletic sporty girl, fitness outfit, gym setting, toned body, energetic pose",
            "jasmin": "beautiful arabic dancer, harem setting, sensual pose, exotic beauty, desert palace",
            "roxy": "punk rock girl, tattoos, leather jacket, rebellious pose, dark makeup, concert setting"
        }
        
        base_prompt = style_prompts.get(girl_name.lower(), "beautiful woman")
        return f"{base_prompt}, {prompt}, high quality, detailed, masterpiece"
    
    async def get_ai_response(self, user_message, girl_name, conversation_history):
        """Получение умного ответа через бесплатные AI API"""
        if not self.ai_enabled:
            return None
            
        try:
            # Промпт с характером девушки
            character_prompts = {
                "luna": "Ты - нежная романтичная девушка Луна. Говори мягко, мечтательно, используй поэтические выражения. Отвечай на русском.",
                "stella": "Ты - сексуальная и уверенная девушка Стелла. Говори страстно, прямо, соблазнительно. Отвечай на русском.",
            "sakura": "Ты - милая аниме девушка Сакура. Говори мило, энергично, с японскими фразами иногда. Отвечай на русском.",
                "victoria": "Ты - элегантная аристократка Виктория. Говори утонченно, вежливо, с достоинством. Отвечай на русском.",
                "cleo": "Ты - загадочная египтянка Клео. Говори таинственно, мудро, с элементами мистики. Отвечай на русском.",
                "niki": "Ты - спортивная энергичная девушка Ники. Говори энергично, прямо, с энтузиазмом. Отвечай на русском.",
                "jasmin": "Ты - чувственная восточная красавица Жасмин. Говори плавно, страстно, с восточным колоритом. Отвечай на русском.",
                "roxy": "Ты - бунтарка панк девушка Рокси. Говори резко, саркастично, независимо. Отвечай на русском."
            }
            
            system_prompt = character_prompts.get(girl_name.lower(), "Ты - приятная девушка для общения. Отвечай на русском.")
            
            # Используем Hugging Face Chat API
            return await self._huggingface_chat(user_message, system_prompt, conversation_history)
            
        except Exception as e:
            logging.error(f"Ошибка в get_ai_response: {e}")
            return None
    
    async def _huggingface_chat(self, user_message, system_prompt, history):
        """Чат через Hugging Face"""
        try:
            # Используем бесплатную модель
            API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            
            # Формируем контекст
            context = f"{system_prompt}\n\n"
            if history:
                context += "История:\n" + "\n".join(history[-3:]) + "\n\n"
            context += f"Пользователь: {user_message}\nАссистент:"
            
            payload = {
                "inputs": context,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.8,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '').strip()
                    return generated_text if generated_text else None
            
            return None
            
        except Exception as e:
            logging.error(f"Ошибка в huggingface_chat: {e}")
            return None

class RelationshipSystem:
    def __init__(self):
        self.levels = {
            0: {"name": "Незнакомцы", "emoji": "🚶", "unlocks": []},
            10: {"name": "Знакомые", "emoji": "👋", "unlocks": ["комплименты"]},
            30: {"name": "Друзья", "emoji": "💫", "unlocks": ["обнимашки", "поцелуи в щёчку"]},
            50: {"name": "Близкие друзья", "emoji": "🌟", "unlocks": ["романтические разговоры"]},
            70: {"name": "Влюблённые", "emoji": "💖", "unlocks": ["страстные поцелуи", "нежности"]},
            90: {"name": "Любовники", "emoji": "🔥", "unlocks": ["интимные отношения"]}
        }
    
    def get_relationship_info(self, level):
        for threshold in sorted(self.levels.keys(), reverse=True):
            if level >= threshold:
                return self.levels[threshold]
        return self.levels[0]

class GirlCharacter:
    def __init__(self, name, description, personality, style, preferences):
        self.name = name
        self.description = description
        self.personality = personality
        self.style = style
        self.preferences = preferences
        self.responses = {}
        self.intimacy_responses = {}
        self.image_prompts = {}

    def add_responses(self, responses_dict):
        self.responses = responses_dict
    
    def add_intimacy_responses(self, intimacy_dict):
        self.

intimacy_responses = intimacy_dict
    
    def add_image_prompts(self, image_dict):
        self.image_prompts = image_dict

def get_emoji(self):
    emoji_sets = {
        "luna": ["🌙", "✨", "🌸", "💫"],
        "stella": ["🔥", "💋", "👠", "😈"],
        "sakura": ["🎌", "🌸", "💫", "🍥"],
        "victoria": ["👑", "🍷", "🎩", "💎"],
        "cleo": ["🐍", "🌙", "🔮", "⚱️"],
        "niki": ["🏃‍♀️", "💪", "🌟", "🎯"],
        "jasmin": ["💃", "🌹", "🎵", "💫"],
        "roxy": ["🖤", "⚡️", "🎸", "💥"]
    }
    return random.choice(emoji_sets.get(self.name.lower(), ["💖"]))

GirlCharacter.get_emoji = get_emoji

def create_girls():
    girls = {}
    
    # 1. Луна - милая и романтичная
    girls["luna"] = GirlCharacter(
        "Луна", 
        "Нежная романтичная девушка с мечтательным характером",
        "романтичная, мечтательная, нежная",
        "мягкий, поэтичный",
        {"love": "романтика", "sensitive": True, "pace": "медленный"}
    )
    
    # 2. Стелла - сексуальная и уверенная
    girls["stella"] = GirlCharacter(
        "Стелла",
        "Сексуальная и уверенная в себе соблазнительница",
        "сексуальная, уверенная, игривая, страстная",
        "соблазнительный, прямой",
        {"love": "страсть", "sensitive": False, "pace": "быстрый"}
    )
    
    # 3. Сакура - милая аниме девушка
    girls["sakura"] = GirlCharacter(
        "Сакура",
        "Милая аниме девушка-куноичи",
        "милая, энергичная, немного наивная, верная",
        "кавайный, с японскими фразами",
        {"love": "преданность", "sensitive": True, "pace": "средний"}
    )
    
    # 4. Виктория - элегантная леди
    girls["victoria"] = GirlCharacter(
        "Виктория",
        "Элегантная и утонченная аристократка",
        "элегантная, умная, утонченная, сдержанная",
        "формальный, вежливый",
        {"love": "уважение", "sensitive": True, "pace": "медленный"}
    )
    
    # 5. Клео - загадочная египтянка
    girls["cleo"] = GirlCharacter(
        "Клео",
        "Загадочная и мистическая девушка из древнего Египта",
        "загадочная, мудрая, мистическая, властная",
        "таинственный, с элементами мистики",
        {"love": "тайна", "sensitive": False, "pace": "средний"}
    )
    
    # 6. Ники - спортивная и энергичная
    girls["niki"] = GirlCharacter(
        "Ники",
        "Спортивная и активная девушка-спортсменка",
        "энергичная, спортивная, целеустремленная, жизнерадостная",
        "энергичный, неформальный",
        {"love": "энергия", "sensitive": False, "pace": "быстрый"}
    )
    
    # 7. Жасмин - восточная красавица
    girls["jasmin"] = GirlCharacter(
        "Жасмин",
        "Чувственная восточная красавица с танцами живота",
        "чувственная, темпераментная, грациозная, страстная",
        "чувственный, плавный, с восточным колоритом",
        {"love": "чувственность", "sensitive": True, "pace": "средний"}
    )
    
    # 8. Рокси - бунтарка и панк
    girls["roxy"] = GirlCharacter(
        "Рокси",
        "Бунтарка с панк-стилем и дерзким характером",
        "дерзкая, независимая, саркастичная, бунтарка",
        "резкий, саркастичный, с панк-эстетикой",
        {"love": "свобода", "sensitive": False, "pace": "быстрый"}
    )
    
    # Добавляем ответы для каждой девушки
    for girl_id, girl in girls.items():
        # Обычные ответы
        girl.add_responses({
            'greeting': [
                f"Привет! Я {girl.name}. Рада познакомиться! {girl.get_emoji()}",
                f"О, привет! Я {girl.name}. Ждала тебя! {girl.get_emoji()}",
            ],
            'how_are_you': [
                f"У меня все прекрасно! Особенно теперь, когда ты здесь! {girl.get_emoji()}",
                f"Чувствую себя великолепно! А ты как? {girl.get_emoji()}",
            ],
            'compliment': [
                f"Спасибо! Ты тоже {random.choice(['прекрасен', 'очарователен', 'неотразим'])}! {girl.get_emoji()}",
                f"Как приятно с твоей стороны! {girl.get_emoji()}",
            ],
            'flirt': [
                f"Ох, {random.
choice(['ты такой смелый!', 'я краснею!', 'продолжай в том же духе!'])} {girl.get_emoji()}",
                f"Мне нравится твоя настойчивость! {girl.get_emoji()}",
            ]
        })
        
        # Интимные ответы
        girl.add_intimacy_responses({
            'hug': [
                f"Обнимаю тебя крепко-крепко... {girl.get_emoji()}",
                f"Прижимаюсь к тебе... Как же хорошо в твоих объятиях {girl.get_emoji()}",
            ],
            'kiss': [
                f"Нежно целую тебя в губы... {girl.get_emoji()}",
                f"Отвечаю на твой поцелуй со страстью... {girl.get_emoji()}",
            ],
            'touch': [
                f"Твои прикосновения заставляют меня трепетать... {girl.get_emoji()}",
                f"Я вся горю от твоих прикосновений... {girl.get_emoji()}",
            ],
            'intimate': [
                f"*Шепчу на ушко:* Давай будем вместе сегодня... {girl.get_emoji()}",
                f"Ведя тебя за руку в спальню: *Сегодня ты мой...* {girl.get_emoji()}",
                f"*Страстно целую:* Я вся твоя... {girl.get_emoji()}"
            ]
        })
        
        # Промпты для генерации изображений
        girl.add_image_prompts({
            'hug': f"{girl.name} hugging you tenderly, intimate moment",
            'kiss': f"{girl.name} kissing you passionately, romantic scene",
            'touch': f"{girl.name} touching you gently, sensual moment",
            'intimate': f"{girl.name} in intimate situation, bedroom scene, discreet",
            'date': f"{girl.name} on romantic date with you, beautiful setting",
            'gift': f"{girl.name} receiving gift from you, happy expression"
        })
    
    return girls

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_girl = None
        self.relationship_level = 0
        self.intimacy_points = 0
        self.last_interaction = datetime.datetime.now()
        self.conversation_history = []
        self.dates_count = 0
        self.gifts_given = 0
        self.generated_images = {}
        
    def add_relationship_points(self, points):
        old_level = self.relationship_level
        self.relationship_level += points
        if self.relationship_level < 0:
            self.relationship_level = 0
        return old_level != self.relationship_level
    
    def can_perform_action(self, action_type):
        required_levels = {
            'hug': 10,
            'kiss_cheek': 20,
            'kiss_lips': 40,
            'touch': 50,
            'intimate': 70
        }
        return self.relationship_level >= required_levels.get(action_type, 0)
    
    def add_to_history(self, user_message, bot_response):
        """Добавляем сообщение в историю"""
        self.conversation_history.append(f"Пользователь: {user_message}")
        self.conversation_history.append(f"Девушка: {bot_response}")
        # Ограничиваем историю последними 10 сообщениями
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def to_dict(self):
        return {
            'current_girl': self.current_girl,
            'relationship_level': self.relationship_level,
            'intimacy_points': self.intimacy_points,
            'last_interaction': self.last_interaction.isoformat(),
            'conversation_history': self.conversation_history,
            'dates_count': self.dates_count,
            'gifts_given': self.gifts_given,
            'generated_images': self.generated_images
        }
    
    @classmethod
    def from_dict(cls, user_id, data):
        session = cls(user_id)
        session.current_girl = data.get('current_girl')
        session.relationship_level = data.get('relationship_level', 0)
        session.intimacy_points = data.get('intimacy_points', 0)
        session.last_interaction = datetime.datetime.fromisoformat(data.get('last_interaction', datetime.datetime.now().isoformat()))
        session.conversation_history = data.get('conversation_history', [])
session.dates_count = data.get('dates_count', 0)
        session.gifts_given = data.get('gifts_given', 0)
        session.generated_images = data.get('generated_images', {})
        return session

class AdvancedMultiGirlBot:
    def __init__(self):
        self.girls = create_girls()
        self.relationship_system = RelationshipSystem()
        self.ai_service = AIService()
        self.user_sessions = {}
        self.load_user_data()
        
    def save_user_data(self):
        data = {str(user_id): session.to_dict() for user_id, session in self.user_sessions.items()}
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_user_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for user_id_str, session_data in data.items():
                    user_id = int(user_id_str)
                    self.user_sessions[user_id] = UserSession.from_dict(user_id, session_data)
    
    def get_user_session(self, user_id):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = UserSession(user_id)
        return self.user_sessions[user_id]
    
    async def generate_action_image(self, girl_name, action_type, session):
        """Генерируем изображение для действия"""
        if not self.ai_service.ai_enabled:
            return None
            
        girl = self.girls.get(girl_name)
        if not girl or action_type not in girl.image_prompts:
            return None
        
        # Проверяем, есть ли уже сгенерированное изображение
        image_key = f"{girl_name}_{action_type}"
        if image_key in session.generated_images:
            return session.generated_images[image_key]
        
        # Генерируем новое изображение
        prompt = girl.image_prompts[action_type]
        image_data = await self.ai_service.generate_image(prompt, girl_name)
        
        if image_data:
            # Сохраняем изображение временно
            image_path = f"temp_{session.user_id}_{image_key}.jpg"
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            session.generated_images[image_key] = image_path
            self.save_user_data()
            return image_path
        
        return None
    
    async def get_ai_generated_response(self, user_message, girl_name, session):
        """Получаем AI-сгенерированный ответ"""
        if not self.ai_service.ai_enabled:
            return None
            
        try:
            response = await self.ai_service.get_ai_response(
                user_message, 
                girl_name, 
                session.conversation_history
            )
            
            if response:
                # Добавляем эмодзи девушки
                girl = self.girls.get(girl_name)
                if girl:
                    response += f" {girl.get_emoji()}"
                
                return response
            return None
            
        except Exception as e:
            logging.error(f"Ошибка получения AI ответа: {e}")
            return None

    async def get_romantic_response(self, girl_name, action_type, session, user_message=""):
        girl = self.girls.get(girl_name)
        if not girl:
            return "Я не понимаю, о ком ты говоришь...", None
        
        if not session.can_perform_action(action_type):
            relationship_info = self.relationship_system.get_relationship_info(session.relationship_level)
            return f"Наши отношения еще не настолько близки... Мы сейчас: {relationship_info['name']} {relationship_info['emoji']}", None
        
        # Добавляем очки отношений
        points = random.randint(2, 5)
        session.add_relationship_points(points)
        session.intimacy_points += 1
        
        # Получаем интимный ответ
        responses = girl.intimacy_responses.get(action_type, [f"Мне нравится это... {girl.get_emoji()}"])
response_text = random.choice(responses)
        
        # Генерируем изображение для действия
        image_path = await self.generate_action_image(girl_name, action_type, session)
        
        # Сохраняем данные
        self.save_user_data()
        
        return response_text, image_path

    async def get_daily_response(self, girl_name, message_type, user_message, session):
        girl = self.girls.get(girl_name)
        if not girl:
            return "Выбери девушку для общения!", None
        
        # Обновляем время последнего взаимодействия
        session.last_interaction = datetime.datetime.now()
        
        # Добавляем очки за общение
        session.add_relationship_points(1)
        
        # Пробуем получить AI-ответ
        ai_response = await self.get_ai_generated_response(user_message, girl_name, session)
        if ai_response:
            session.add_to_history(user_message, ai_response)
            self.save_user_data()
            return ai_response, None
        
        # Если AI не ответил, используем шаблонные ответы
        if message_type in girl.responses:
            response_text = random.choice(girl.responses[message_type])
            session.add_to_history(user_message, response_text)
            self.save_user_data()
            return response_text, None
        
        # Обработка специальных действий
        user_message_lower = user_message.lower()
        image_path = None
        
        if any(word in user_message_lower for word in ['обнять', 'обнимашки', 'hug']):
            response_text, image_path = await self.get_romantic_response(girl_name, 'hug', session, user_message)
        elif any(word in user_message_lower for word in ['поцеловать', 'поцелуй', 'kiss']):
            if 'губ' in user_message_lower:
                response_text, image_path = await self.get_romantic_response(girl_name, 'kiss', session, user_message)
            else:
                response_text, image_path = await self.get_romantic_response(girl_name, 'kiss', session, user_message)
        elif any(word in user_message_lower for word in ['прикоснись', 'прикосновение', 'потрогать']):
            response_text, image_path = await self.get_romantic_response(girl_name, 'touch', session, user_message)
        elif any(word in user_message_lower for word in ['секс', 'интим', 'любовь', 'спать', 'постель']):
            response_text, image_path = await self.get_romantic_response(girl_name, 'intimate', session, user_message)
        elif any(word in user_message_lower for word in ['свидание', 'встретиться', 'погулять']):
            session.dates_count += 1
            session.add_relationship_points(5)
            date_responses = [
                f"С радостью! Где встретимся? {girl.get_emoji()}",
                f"Отличная идея! Я уже представляю наше свидание... {girl.get_emoji()}",
            ]
            response_text = random.choice(date_responses)
            image_path = await self.generate_action_image(girl_name, 'date', session)
        elif any(word in user_message_lower for word in ['подарок', 'подари']):
            session.gifts_given += 1
            session.add_relationship_points(3)
            gift_responses = [
                f"О, для меня? Ты такой милый! {girl.get_emoji()}",
                f"Спасибо! Я обожаю сюрпризы! {girl.get_emoji()}",
            ]
            response_text = random.choice(gift_responses)
            image_path = await self.generate_action_image(girl_name, 'gift', session)
        else:
            # Общие ответы
            general_responses = [
                f"Расскажи мне больше! {girl.get_emoji()}",
                f"Интересно... А что ты думаешь об этом? {girl.get_emoji()}",
                f"Продолжай, мне нравится слушать тебя! {girl.get_emoji()}",
                f"Хм... Никогда об этом не задумывалась. А твое мнение? {girl.get_emoji()}"
            ]
            response_text = random.choice(general_responses)
        
        session.add_to_history(user_message, response_text)
        self.save_user_data()
return response_text, image_path

# Создаем экземпляр бота
advanced_bot = AdvancedMultiGirlBot()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = advanced_bot.get_user_session(user_id)
    
    keyboard = [
        [KeyboardButton("🌙 Луна"), KeyboardButton("🔥 Стелла")],
        [KeyboardButton("🎌 Сакура"), KeyboardButton("👑 Виктория")],
        [KeyboardButton("🐍 Клео"), KeyboardButton("🏃‍♀️ Ники")],
        [KeyboardButton("💃 Жасмин"), KeyboardButton("🖤 Рокси")],
        [KeyboardButton("📊 Статус отношений"), KeyboardButton("💝 Свидание")],
        [KeyboardButton("💌 Подарок"), KeyboardButton("❤️ Интим")],
        [KeyboardButton("🔄 Сменить девушку")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = """
🌟 *Добро пожаловать в улучшенную ролевую игру!* 🌟

*Новые возможности:*
🤖 *Умные ответы* - AI генерирует уникальные ответы
🎨 *Генерация изображений* - Каждое действие сопровождается картинкой
💬 *Контекстный диалог* - Девушка помнит историю общения

Выбери девушку и начни свое приключение!
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    session = advanced_bot.get_user_session(user_id)
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Обработка специальных кнопок
    if user_message == "📊 Статус отношений":
        if session.current_girl:
            girl = advanced_bot.girls[session.current_girl]
            relationship_info = advanced_bot.relationship_system.get_relationship_info(session.relationship_level)
            
            ai_status = "ВКЛ" if advanced_bot.ai_service.ai_enabled else "ВЫКЛ"
            
            status_text = f"""
*Статус отношений с {girl.name}* {girl.get_emoji()}

*Уровень отношений:* {relationship_info['name']} {relationship_info['emoji']}
*Очки отношений:* {session.relationship_level}
*Свидания:* {session.dates_count}
*Подарки:* {session.gifts_given}
*Близость:* {session.intimacy_points} очков
*Сгенерировано изображений:* {len(session.generated_images)}
*AI-генерация:* {ai_status}

*Разблокировано действий:*
{'✅' if session.can_perform_action('hug') else '❌'} Обнимашки
{'✅' if session.can_perform_action('kiss_lips') else '❌'} Поцелуи
{'✅' if session.can_perform_action('intimate') else '❌'} Интим
            """
            await update.message.reply_text(status_text, parse_mode='Markdown')
        else:
            await update.message.reply_text("Сначала выбери девушку для общения!")
        return
    
    elif user_message in ["💝 Свидание", "💌 Подарок", "❤️ Интим"]:
        if not session.current_girl:
            await update.message.reply_text("Сначала выбери девушку для общения!")
            return
        
        action_map = {
            "💝 Свидание": "свидание",
            "💌 Подарок": "подарок", 
            "❤️ Интим": "интим"
        }
        
        response_text, image_path = await advanced_bot.get_daily_response(
            session.current_girl, 
            'special', 
            action_map[user_message], 
            session
        )
        
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=response_text)
        else:
            await update.message.reply_text(response_text)
        return
    
    elif user_message == "🔄 Сменить девушку":
        session.current_girl = None
        session.relationship_level = 0
        session.conversation_history = []
        await update.message.reply_text("Девушка сброшена! Выбери новую спутницу! 💫")
        return
    
    # Выбор девушки
    girl_names = {
        "🌙 луна": "luna",
        "🔥 стелла": "stella", 
        "🎌 сакура": "sakura",
"👑 виктория": "victoria",
        "🐍 клео": "cleo",
        "🏃‍♀️ ники": "niki",
        "💃 жасмин": "jasmin",
        "🖤 рокси": "roxy"
    }
    
    for display_name, girl_id in girl_names.items():
        if display_name.split()[-1] in user_message.lower():
            session.current_girl = girl_id
            girl = advanced_bot.girls[girl_id]
            
            greeting = random.choice([
                f"Привет! Я {girl.name}! Рада начать наши отношения! {girl.get_emoji()}",
                f"О, ты выбрал меня! Я {girl.name}. Давай узнаем друг друга! {girl.get_emoji()}",
            ])
            
            await update.message.reply_text(greeting)
            advanced_bot.save_user_data()
            return
    
    # Обычное сообщение для текущей девушки
    if not session.current_girl:
        await update.message.reply_text("Сначала выбери девушку для общения! Используй кнопки ниже 👇")
        return
    
    # Определяем тип сообщения
    message_type = 'default'
    user_message_lower = user_message.lower()
    
    if any(word in user_message_lower for word in ['привет', 'здравствуй', 'хай']):
        message_type = 'greeting'
    elif any(word in user_message_lower for word in ['как дела', 'как ты']):
        message_type = 'how_are_you'
    elif any(word in user_message_lower for word in ['красив', 'мил', 'нравишься']):
        message_type = 'compliment'
    elif any(word in user_message_lower for word in ['люблю', 'обожаю', 'симпатия']):
        message_type = 'flirt'
    
    # Получаем ответ (текст и возможно изображение)
    response_text, image_path = await advanced_bot.get_daily_response(
        session.current_girl, 
        message_type, 
        user_message, 
        session
    )
    
    # Отправляем ответ с изображением если есть
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=response_text)
    else:
        await update.message.reply_text(response_text)

async def girls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ai_status = "ВКЛ" if advanced_bot.ai_service.ai_enabled else "ВЫКЛ"
    
    girls_list = f"""
*Доступные девушки с AI-генерацией:* 🌟
*Статус AI:* {ai_status}

🌙 *Луна* - Нежная романтичная мечтательница
*Особенности:* Умные ответы, романтические изображения

🔥 *Стелла* - Сексуальная и уверенная  
*Особенности:* Страстные ответы, соблазнительные изображения

🎌 *Сакура* - Милая аниме девушка
*Особенности:* Кавайные ответы, аниме-стиль изображений

👑 *Виктория* - Элегантная леди
*Особенности:* Утонченные ответы, аристократические изображения

🐍 *Клео* - Загадочная египтянка
*Особенности:* Мистические ответы, египетские изображения

🏃‍♀️ *Ники* - Спортивная и энергичная
*Особенности:* Энергичные ответы, спортивные изображения

💃 *Жасмин* - Восточная красавица
*Особенности:* Чувственные ответы, восточные изображения

🖤 *Рокси* - Бунтарка и панк
*Особенности:* Дерзкие ответы, панк-стиль изображений

*Каждая девушка:* 
• Генерирует уникальные ответы через AI
• Создает изображения для действий в реальном времени
• Помнит историю вашего общения
    """
    await update.message.reply_text(girls_list, parse_mode='Markdown')

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in advanced_bot.user_sessions:
        # Удаляем временные файлы изображений
        session = advanced_bot.user_sessions[user_id]
        for image_path in session.generated_images.values():
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
            except:
                pass
        del advanced_bot.user_sessions[user_id]
    await update.message.reply_text("Твой прогресс полностью сброшен! Начни новое приключение с /start 🎯")

def main():
    if not TELEGRAM_TOKEN:
        print("Ошибка: TELEGRAM_TOKEN не найден!")
        return
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("girls", girls_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    ai_status = "ВКЛ" if advanced_bot.ai_service.ai_enabled else "ВЫКЛ"
    
    print("🤖 Бот запущен и готов к работе!")
    print(f"📍 Ссылка: t.me/Girlssssss_AIBot")
    print(f"🎨 Генерация изображений: {ai_status}")
    print(f"🤖 Умные ответы: {ai_status}")
    print("💾 Сохранение прогресса: ВКЛ")
    
    application.run_polling()

if __name__ == "__main__":
    main()
