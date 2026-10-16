import config_data.config as config
from telegram.ext import ApplicationBuilder
from telegram.request import HTTPXRequest

# Увеличиваем таймауты для работы в России
request = HTTPXRequest(
    connect_timeout=30.0,
    read_timeout=30.0,
    write_timeout=30.0,
    # proxy_url="socks5://localhost:1080"  # Раскомментируйте, если используете прокси
)

application = (
    ApplicationBuilder()
    .token(config.TOKEN)
    .request(request)
    .build()
)
