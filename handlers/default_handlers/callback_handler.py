# handlers/default_handlers/callback_handler.py
import logging
from telegram import Update, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from utils.apartments_data import APARTMENTS
from keyboards.reply import center_keyboard, sea_keyboard, sleep_keyboard, district_keyboard
from config_data.config import WEBSITE

logger = logging.getLogger(__name__)


async def show_apartment(update: Update, apt_key: str):
    """Показ квартиры + кнопка бронирования"""
    query = update.callback_query
    apt = APARTMENTS.get(apt_key)

    if not apt:
        await query.message.reply_text("Квартира не найдена 😔")
        return

    photos = apt["photos"]
    caption = apt["caption"]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛎 Забронировать эту квартиру", callback_data=f"book_{apt_key}")]
    ])

    media_group = [InputMediaPhoto(media=photos[0], caption=caption, parse_mode="Markdown")]
    for photo in photos[1:10]:
        media_group.append(InputMediaPhoto(media=photo))

    try:
        await query.message.reply_media_group(media=media_group)
        await query.message.reply_text(
            "Хотите забронировать эту квартиру?",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error sending apartment {apt_key}: {e}")
        await query.message.reply_text("❌ Ошибка при отправке информации о квартире.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главный обработчик inline кнопок"""
    query = update.callback_query
    data = query.data

    logger.info(f"Callback: {data}")

    # Пропускаем callback'и для бронирования и календаря
    if data.startswith("book_") or data.startswith("cal_") or data == "ignore":
        return

    # Обрабатываем старые кнопки
    if data in ["confirm_booking", "cancel_booking"]:
        await query.answer("⏳ Эта заявка уже обработана", show_alert=True)
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        return

    await query.answer()

    if data == "main_menu":
        from keyboards.reply import main_keyboard
        await query.message.reply_text("🏠 Главное меню", reply_markup=main_keyboard)

    elif data == "district_back":
        try:
            await query.message.delete()
        except Exception:
            pass
        await query.message.reply_text("🌍 Выберите район:", reply_markup=district_keyboard())

    elif data == "district_center":
        await query.edit_message_text("🌆 Квартиры в центре:", reply_markup=center_keyboard())
    elif data == "district_sea":
        await query.edit_message_text("🌊 Квартиры у моря:", reply_markup=sea_keyboard())
    elif data == "district_sleep":
        await query.edit_message_text("🏙 Квартиры в спальных районах:", reply_markup=sleep_keyboard())

    elif data in APARTMENTS:
        await show_apartment(update, data)

    else:
        await query.message.reply_text("Неизвестная команда 🤔")