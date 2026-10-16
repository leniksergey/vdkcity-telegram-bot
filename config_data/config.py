import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
LOG_LEVEL = "INFO"

TELEGRAM_CHANNEL = "@arenda_vdk_city"
WEBSITE = "https://vdkcity.ru"
PHONE = "+7 (924) 265-96-91"

print(f"✅ TOKEN загружен: {'Да' if TOKEN else 'Нет'}")
