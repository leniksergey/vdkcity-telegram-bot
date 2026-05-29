from telegram.ext import Application
from config_data import config

application = Application.builder().token(config.TOKEN).build()