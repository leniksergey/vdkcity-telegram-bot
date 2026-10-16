import asyncio
import logging
import os
import time
import warnings

from telegram.warnings import PTBUserWarning

from utils.logging_filters import MaskTokenFilter

# Настройка логирования ДО импортов проекта
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


_root = logging.getLogger()
for _h in _root.handlers:
    _h.addFilter(MaskTokenFilter())
_root.addFilter(MaskTokenFilter())

warnings.filterwarnings("ignore", category=PTBUserWarning)

from config_data import config  # noqa: E402

logging.getLogger().setLevel(config.LOG_LEVEL)

_httpx_level = logging.INFO if os.getenv("DEBUG") == "1" else logging.WARNING
logging.getLogger("httpx").setLevel(_httpx_level)
logging.getLogger("httpcore").setLevel(_httpx_level)

from telegram.ext import (  # noqa: E402
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from handlers.booking_handlers.booking_handlers import booking_conv  # noqa: E402
from handlers.default_handlers.admin import find_booking, show_bookings, stats  # noqa: E402
from handlers.default_handlers.callback_handler import button_callback  # noqa: E402
from handlers.default_handlers.commands import help_command, history_command  # noqa: E402
from handlers.default_handlers.contacts import contacts  # noqa: E402
from handlers.default_handlers.rules import rules  # noqa: E402
from handlers.default_handlers.start import start  # noqa: E402
from keyboards.reply import district_keyboard  # noqa: E402
from loader import application  # noqa: E402
from utils.database import init_db  # noqa: E402

_log = logging.getLogger(__name__)


def main():
    init_db()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("history", history_command))

    application.add_handler(CommandHandler("bookings", show_bookings))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("find", find_booking))

    application.add_handler(booking_conv)
    application.add_handler(CallbackQueryHandler(button_callback))

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

    _log.info("🤖 Бот VDKcity успешно запущен")
    _log.info("📋 Доступные команды: /start, /help, /history")

    while True:
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            application.run_polling()
        except KeyboardInterrupt:
            _log.info("🛑 Остановка пользователем")
            break
        except Exception:
            _log.exception("❌ Бот упал, перезапуск через 10 секунд")
            time.sleep(10)
        else:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        _log.info("🛑 Бот остановлен пользователем")
