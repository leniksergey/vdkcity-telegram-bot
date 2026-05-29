import logging
from datetime import datetime, timedelta, date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters, \
    CommandHandler

from utils.database import add_booking
from utils.apartments_data import APARTMENTS
from config_data.config import ADMIN_ID
from utils.calendar import get_calendar
from states.booking_states import (
    CHOOSING_CHECKIN, CHOOSING_CHECKOUT, CHOOSING_GUESTS,
    ASKING_NAME, ASKING_PHONE, CONFIRMATION
)

logger = logging.getLogger(__name__)


async def start_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    apt_key = query.data.replace("book_", "")
    context.user_data['apt_key'] = apt_key
    apt = APARTMENTS.get(apt_key)

    if not apt:
        await query.message.reply_text("❌ Квартира не найдена.")
        return ConversationHandler.END

    context.user_data['booking_apt_name'] = apt['name']

    today = date.today()
    await query.message.reply_text(
        f"🏠 {apt['name']}\n\n📅 Выберите **дату заезда**:",
        parse_mode="Markdown",
        reply_markup=get_calendar(today.year, today.month, min_date=today)
    )
    return CHOOSING_CHECKIN


async def calendar_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    parts = data.split("_")
    action = parts[1]

    year = int(parts[2])
    month = int(parts[3])

    min_date = date.today()
    if context.user_data.get('temp_checkout_min_date'):
        min_date = context.user_data['temp_checkout_min_date']

    if action == "prev":
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    elif action == "next":
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    await query.edit_message_reply_markup(
        reply_markup=get_calendar(year, month, min_date=min_date)
    )


async def select_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    _, _, year, month, day = data.split("_")
    checkin_date = date(int(year), int(month), int(day))

    context.user_data['checkin'] = checkin_date.strftime("%d.%m.%Y")
    context.user_data['checkin_obj'] = checkin_date

    next_min_date = checkin_date + timedelta(days=1)

    await query.edit_message_text(
        f"✅ Дата заезда: {context.user_data['checkin']}\n\n📅 Теперь выберите **дату выезда**:",
        parse_mode="Markdown",
        reply_markup=get_calendar(checkin_date.year, checkin_date.month, min_date=next_min_date)
    )
    return CHOOSING_CHECKOUT


async def select_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    _, _, year, month, day = data.split("_")
    checkout_date = date(int(year), int(month), int(day))

    checkin_obj = context.user_data.get('checkin_obj')
    if checkout_date <= checkin_obj:
        await query.answer("Дата выезда должна быть позже даты заезда!", show_alert=True)
        return CHOOSING_CHECKOUT

    context.user_data['checkout'] = checkout_date.strftime("%d.%m.%Y")
    context.user_data['dates'] = f"{context.user_data['checkin']} — {context.user_data['checkout']}"

    await query.edit_message_text(
        f"✅ Даты: {context.user_data['dates']}\n\n👥 Сколько будет гостей? (например: 2)"
    )
    return CHOOSING_GUESTS


async def get_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        guests = int(update.message.text.strip())
        if guests < 1:
            raise ValueError
        context.user_data['guests'] = str(guests)
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите число (например: 2)")
        return CHOOSING_GUESTS

    await update.message.reply_text("👤 Ваше ФИО полностью?")
    return ASKING_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text.strip()
    await update.message.reply_text("📱 Укажите ваш номер телефона:")
    return ASKING_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text.strip()

    data = context.user_data
    apt = APARTMENTS.get(data['apt_key'])

    nights = "—"
    if 'checkin_obj' in data and 'checkout' in data:
        checkout_obj = datetime.strptime(data['checkout'], "%d.%m.%Y").date()
        nights = (checkout_obj - data['checkin_obj']).days

    text = f"""
✅ *Подтверждение бронирования*

🏠 Квартира: {apt['name']}
📅 Даты: {data['dates']} ({nights} ночей)
👥 Гостей: {data['guests']}
👤 Имя: {data['name']}
📱 Телефон: {data['phone']}
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Подтвердить заявку", callback_data="confirm_booking")],
        [InlineKeyboardButton("❌ Отменить", callback_data="cancel_booking")]
    ])

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    return CONFIRMATION


async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = context.user_data
    apt = APARTMENTS.get(data['apt_key'])

    nights = "—"
    if 'checkin_obj' in data and 'checkout' in data:
        checkout_obj = datetime.strptime(data['checkout'], "%d.%m.%Y").date()
        nights = (checkout_obj - data['checkin_obj']).days

    booking_data = {
        'apartment_name': apt['name'],
        'checkin': data.get('checkin'),
        'checkout': data.get('checkout'),
        'nights': nights if nights != "—" else 0,
        'guests': int(data.get('guests')),
        'customer_name': data.get('name'),
        'customer_phone': data.get('phone'),
        'user_id': query.from_user.id,
        'username': query.from_user.username
    }

    booking_id = add_booking(booking_data)
    print(f"📝 Заявка #{booking_id} сохранена в БД")

    booking_text = f"""
🛎 **НОВАЯ ЗАЯВКА НА БРОНИРОВАНИЕ!**

🏠 Квартира: {apt['name']}
📅 Даты: {data.get('dates')} ({nights} ночей)
👥 Гостей: {data.get('guests')}
👤 Имя: {data.get('name')}
📱 Телефон: {data.get('phone')}
🆔 Пользователь: @{query.from_user.username or query.from_user.id}
    """

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=booking_text,
            parse_mode="Markdown"
        )
        print(f"✅ Заявка отправлена на {ADMIN_ID}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        await query.message.reply_text("⚠️ Ошибка при отправке заявки. Пожалуйста, свяжитесь с нами по телефону.")
        context.user_data.clear()
        return ConversationHandler.END

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    await query.message.reply_text(
        "✅ Заявка успешно отправлена!\nМы свяжемся с вами в ближайшее время."
    )

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Отменено")

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    await query.message.reply_text("❌ Бронирование отменено.")

    context.user_data.clear()
    return ConversationHandler.END


booking_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_booking, pattern="^book_")],
    states={
        CHOOSING_CHECKIN: [
            CallbackQueryHandler(calendar_navigation, pattern="^cal_(prev|next)_"),
            CallbackQueryHandler(select_checkin, pattern="^cal_day_"),
        ],
        CHOOSING_CHECKOUT: [
            CallbackQueryHandler(calendar_navigation, pattern="^cal_(prev|next)_"),
            CallbackQueryHandler(select_checkout, pattern="^cal_day_"),
        ],
        CHOOSING_GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_guests)],
        ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ASKING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        CONFIRMATION: [
            CallbackQueryHandler(confirm_booking, pattern="^confirm_booking$"),
            CallbackQueryHandler(cancel_booking, pattern="^cancel_booking$"),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_booking)],
    name="booking_conversation",
    allow_reentry=True
)