import logging
import os

from telegram import Update
from telegram.ext import ContextTypes

from config_data.config import WEBSITE, TELEGRAM_CHANNEL
from keyboards.reply import main_keyboard

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = os.path.join(os.path.dirname(__file__), "..", "..", "static", "ETVmc.jpg")
    caption = (
        f"🌐 Наш сайт: {WEBSITE}\n"
        f"👉 Telegram-канал: {TELEGRAM_CHANNEL}\n\n"
        f"👇 Используйте меню ниже для навигации:"
    )

    if not os.path.exists(photo_path):
        logger.warning("Файл не найден: %s", photo_path)
        await update.message.reply_text(
            f"🏠 Добро пожаловать в VDKcity!\n\n{caption}",
            reply_markup=main_keyboard,
        )
        return

    try:
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=main_keyboard,
            )
    except Exception:
        logger.exception("Ошибка отправки фото")
        await update.message.reply_text(
            f"🏠 Добро пожаловать в VDKcity!\n\n{caption}",
            reply_markup=main_keyboard,
        )
