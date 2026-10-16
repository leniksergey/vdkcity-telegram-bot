from telegram.ext import ApplicationBuilder
from telegram.request import HTTPXRequest

import config_data.config as config

request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0, write_timeout=30.0)

builder = ApplicationBuilder().token(config.TOKEN).request(request)
if config.API_BASE_URL:
    builder = builder.base_url(config.API_BASE_URL)
application = builder.build()
