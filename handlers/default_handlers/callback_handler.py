# handlers/default_handlers/callback_handler.py
import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    Update,
)
from telegram.ext import ContextTypes

from keyboards.reply import (
    center_keyboard,
    district_keyboard,
    sea_keyboard,
    sleep_keyboard,
)
from utils.apartments_data import APARTMENTS

logger = logging.getLogger(__name__)


def _reply_text_safe(message, text: str, **kwargs):
    """Безопасная отправка текста"""
    if isinstance(message, Message):
        return message.reply_text(text, **kwargs)
    return None


def _reply_media_group_safe(message, media_group):
    """Безопасная отправка медиагруппы"""
    if isinstance(message, Message):
        return message.reply_media_group(media_group)
    return None


async def show_apartment(update: Update, apt_key: str):
    """Показ квартиры: 4 фото + кнопка 'Все фото'"""
    query = update.callback_query
    await query.answer()

    apt = APARTMENTS.get(apt_key)
    if not apt:
        await _reply_text_safe(query.message, "Квартира не найдена 😔")
        return

    photos = apt["photos"]
    caption = apt["caption"]

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🛎 Забронировать эту квартиру", callback_data=f"book_{apt_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    "📸 Показать все фото", callback_data=f"allphotos_{apt_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    "← Назад к списку квартир", callback_data="back_to_list"
                )
            ],
        ]
    )

    # Показываем только первые 4 фото
    limited_photos = photos[:4]

    media_group = [
        InputMediaPhoto(media=limited_photos[0], caption=caption, parse_mode="Markdown")
    ]
    for photo in limited_photos[1:]:
        media_group.append(InputMediaPhoto(media=photo))

    try:
        await _reply_media_group_safe(query.message, media_group)
        await _reply_text_safe(
            query.message, "Хотите забронировать эту квартиру?", reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error sending apartment {apt_key}: {e}")
        await _reply_text_safe(query.message, "❌ Ошибка при отправке.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главный обработчик inline кнопок"""
    query = update.callback_query
    data = query.data

    if not data:
        return

    logger.info(f"Callback: {data}")

    # Пропускаем callback'и бронирования и календаря
    if data.startswith("book_") or data.startswith("cal_") or data == "ignore":
        return

    # Обработка подтверждения/отмены брони
    if data in ["confirm_booking", "cancel_booking"]:
        await query.answer("⏳ Эта заявка уже обработана", show_alert=True)
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        return

    await query.answer()

    # ==================== ОСНОВНАЯ ЛОГИКА ====================

    if data == "main_menu":
        from keyboards.reply import main_keyboard

        await _reply_text_safe(
            query.message, "🏠 Главное меню", reply_markup=main_keyboard
        )

    elif data == "back_to_list":
        await handle_back_to_list(query, context)

    elif data == "district_center":
        context.user_data["last_district"] = "district_center"
        await query.edit_message_text(
            "🌆 Квартиры в центре:", reply_markup=center_keyboard()
        )

    elif data == "district_sea":
        context.user_data["last_district"] = "district_sea"
        await query.edit_message_text(
            "🌊 Квартиры у моря:", reply_markup=sea_keyboard()
        )

    elif data == "district_sleep":
        context.user_data["last_district"] = "district_sleep"
        await query.edit_message_text(
            "🏙 Квартиры в спальных районах:", reply_markup=sleep_keyboard()
        )

    elif data == "district_back":
        await _reply_text_safe(
            query.message, "🌍 Выберите район:", reply_markup=district_keyboard()
        )

    elif (
        data.startswith("sleep_")
        or data.startswith("sea_")
        or data.startswith("center_")
    ):
        # Это квартиры — передаём в show_apartment
        await show_apartment(update, data)

    elif data.startswith("allphotos_"):
        apt_key = data.replace("allphotos_", "")

        apt = APARTMENTS.get(apt_key)

        if not apt or len(apt["photos"]) <= 4:
            await query.answer("Больше фотографий нет")

            return

        # Отправляем оставшиеся фото

        remaining_photos = apt["photos"][4:]

        media_group = [InputMediaPhoto(media=photo) for photo in remaining_photos]

        try:
            await _reply_media_group_safe(query.message, media_group)

            await query.answer("✅ Все фото отправлены")

        except Exception as e:
            logger.error(f"Error sending all photos: {e}")

            await query.answer("Не удалось отправить фото")


async def handle_back_to_list(query, context):
    """Возврат к списку квартир"""
    await query.answer("↩️ Возвращаемся к списку...")

    try:
        if isinstance(query.message, Message):
            await query.message.delete()
    except Exception:
        pass

    last_district = context.user_data.get("last_district")

    if last_district == "district_center":
        text = "🌆 Квартиры в центре:"
        markup = center_keyboard()
    elif last_district == "district_sleep":
        text = "🏙 Квартиры в спальных районах:"
        markup = sleep_keyboard()
    else:
        text = "🌊 Квартиры у моря:"
        markup = sea_keyboard()

    await _reply_text_safe(query.message, text, reply_markup=markup)
