import logging
import asyncio
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters
from loader import application
from config_data import config

# Подключаем обработчики через их точное расположение
from handlers.default_handlers.start import start
from handlers.default_handlers.rules import rules
from handlers.default_handlers.contacts import contacts
from handlers.default_handlers.callback_handler import button_callback
from handlers.default_handlers.commands import help_command, history_command
from handlers.default_handlers.admin import show_bookings, stats, find_booking
from handlers.booking_handlers.booking_handlers import booking_conv

from keyboards.reply import district_keyboard
from utils.database import init_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=config.LOG_LEVEL,
)


def main():
    init_db()

    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("history", history_command))

    # Админ-команды
    application.add_handler(CommandHandler("bookings", show_bookings))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("find", find_booking))

    # Бронирование
    application.add_handler(booking_conv)

    # Обработчики кнопок
    application.add_handler(CallbackQueryHandler(button_callback))

    # Кнопки меню
    application.add_handler(MessageHandler(filters.Regex("^📋 Правила$"), rules))
    application.add_handler(MessageHandler(filters.Regex("^📞 Контакты$"), contacts))
    application.add_handler(
        MessageHandler(
            filters.Regex("^🏠 Квартиры$"),
            lambda u, c: u.message.reply_text(
                "🌍 Выберите район:", reply_markup=district_keyboard()
            ),
        )
    )
    application.add_handler(
        MessageHandler(
            filters.Regex("^🌐 Сайт$"),
            lambda u, c: u.message.reply_text(f"🌐 {config.WEBSITE}"),
        )
    )

    print("🤖 Бот VDKcity успешно запущен!")
    print("📋 Доступные команды: /start, /help, /history")
    asyncio.set_event_loop(asyncio.new_event_loop())
    application.run_polling()


if __name__ == "__main__":
    main()
