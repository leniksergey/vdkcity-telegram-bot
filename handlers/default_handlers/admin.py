from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_bookings, get_statistics, get_booking_by_id, update_booking_status
from config_data.config import ADMIN_ID


async def show_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать последние заявки"""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет доступа")
        return

    bookings = get_bookings(limit=10)

    if not bookings:
        await update.message.reply_text("📭 Нет заявок")
        return

    text = "📋 *Последние заявки:*\n\n"
    for b in bookings:
        text += f"`#{b[0]}` | *{b[1]}*\n"
        text += f"📅 {b[2]} — {b[3]}\n"
        text += f"👤 {b[4]} | 📞 {b[5]}\n"
        text += f"📊 {b[6]}\n"
        text += f"⏰ {b[7]}\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику"""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет доступа")
        return

    stats = get_statistics()

    text = f"""
📊 *Статистика бронирований*

📝 Всего заявок: {stats['total']}
📅 За сегодня: {stats['today']}

🏆 *Популярные квартиры:*
"""
    for apt, count in stats['popular']:
        text += f"• {apt}: {count}\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def find_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Найти заявку по ID"""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет доступа")
        return

    if not context.args:
        await update.message.reply_text("📝 Укажите ID заявки: `/find 123`", parse_mode="Markdown")
        return

    try:
        booking_id = int(context.args[0])
        booking = get_booking_by_id(booking_id)

        if not booking:
            await update.message.reply_text(f"❌ Заявка #{booking_id} не найдена")
            return

        text = f"""
📋 *Заявка #{booking.id}*

🏠 {booking.apartment_name}
📅 {booking.checkin_date} — {booking.checkout_date} ({booking.nights} ночей)
👥 {booking.guests} гостей

👤 {booking.customer_name}
📞 {booking.customer_phone}
🆔 @{booking.username or booking.user_id}

⏰ Создана: {booking.created_at.strftime('%d.%m.%Y %H:%M')}
📊 Статус: {booking.status}
"""
        await update.message.reply_text(text, parse_mode="Markdown")

    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")