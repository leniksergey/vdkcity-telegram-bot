import os
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.reply import main_keyboard
from config_data.config import WEBSITE, TELEGRAM_CHANNEL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Исправлено: ищем ETVmc.jpg вместо Gemini_...
    photo_path = os.path.join(os.path.dirname(__file__), "..", "..", "ETVmc.jpg")
    caption = f"🌐 Наш сайт: {WEBSITE}\n👉 Telegram-канал: {TELEGRAM_CHANNEL}\n\n👇 Используйте меню ниже для навигации:"

    if os.path.exists(photo_path):
        try:
            with open(photo_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=caption, reply_markup=main_keyboard)
        except Exception as e:
            print(f"Ошибка отправки фото: {e}")
            await update.message.reply_text(f"🏠 Добро пожаловать в VDKcity!\n\n{caption}", reply_markup=main_keyboard)
    else:
        print(f"Файл не найден: {photo_path}")
        await update.message.reply_text(f"🏠 Добро пожаловать в VDKcity!\n\n{caption}", reply_markup=main_keyboard)