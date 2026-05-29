
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user_bookings, save_user_query
from keyboards.reply import main_keyboard


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    text = """
🤖 *Бот для бронирования квартир VDKcity*

*Доступные команды:*
/start - Запустить главное меню
/help - Показать эту справку
/history - История ваших заявок

*Как забронировать:*
1. Нажмите "🏠 Квартиры"
2. Выберите район
3. Выберите квартиру
4. Нажмите "Забронировать"
5. Выберите даты и заполните форму

📞 Контакты: +7 (924) 265-96-91
🌐 Сайт: https://vdkcity.ru
    """
    await update.message.reply_text(text, parse_mode="Markdown")

    # Сохраняем в историю
    save_user_query(user_id, "/help", None)


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /history - история ваших заявок"""
    user_id = update.effective_user.id
    bookings = get_user_bookings(user_id, limit=10)

    if not bookings:
        await update.message.reply_text("📭 У вас пока нет заявок на бронирование")
        return

    text = "📋 *Ваши заявки:*\n\n"
    for b in bookings:
        text += f"🏠 {b.apartment_name}\n"
        text += f"📅 {b.checkin_date} — {b.checkout_date} ({b.nights} ночей)\n"
        text += f"👥 {b.guests} гостей\n"
        text += f"📊 Статус: {b.status}\n"
        text += f"⏰ {b.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")

    # Сохраняем в историю
    save_user_query(user_id, "/history", None)
