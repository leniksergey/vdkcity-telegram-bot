from telegram import Update
from telegram.ext import ContextTypes
from config_data.config import PHONE, TELEGRAM_CHANNEL

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"📞 <b>Контакты</b>\n\nТелефон: <code>{PHONE}</code>\nНаш Telegram-канал: <a href='{TELEGRAM_CHANNEL}'>{TELEGRAM_CHANNEL}</a>"
    await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)