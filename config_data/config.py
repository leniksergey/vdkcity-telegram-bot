import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

TELEGRAM_CHANNEL = "@arenda_vdk_city"
WEBSITE = "https://vdkcity.ru"
PHONE = "+7 (924) 265-96-91"

if not TOKEN:
    logger.error("❌ TOKEN не задан в .env — бот не сможет работать")
else:
    logger.debug("✅ TOKEN загружен")
