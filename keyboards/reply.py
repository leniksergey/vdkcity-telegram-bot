from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    [
        ["🏠 Квартиры"],
        ["📋 Правила", "📞 Контакты"],
        ["🌐 Сайт"],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


def district_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌆 Центр", callback_data="district_center")],
        [InlineKeyboardButton("🌊 У моря", callback_data="district_sea")],
        [InlineKeyboardButton("🏙 Спальные районы", callback_data="district_sleep")],
        [InlineKeyboardButton("← Главное меню", callback_data="main_menu")]
    ])


def center_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("3-х уровневая на Арбате", callback_data="center_arbat")],
        [InlineKeyboardButton("3-х уровневая в центре", callback_data="center_historical")],
        [InlineKeyboardButton("← Назад к районам", callback_data="district_back")]
    ])


def sea_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("№1 Эгершельд", callback_data="sea_eger1")],
        [InlineKeyboardButton("№2 Эгершельд", callback_data="sea_eger2")],
        [InlineKeyboardButton("№3 Эгершельд", callback_data="sea_eger3")],
        [InlineKeyboardButton("№4 Эгершельд", callback_data="sea_eger4")],
        [InlineKeyboardButton("4-х комнатная Эгершельд", callback_data="sea_4rooms")],
        [InlineKeyboardButton("Уютная студия №1", callback_data="sea_comfy1")],
        [InlineKeyboardButton("Уютная студия №2", callback_data="sea_comfy2")],
        [InlineKeyboardButton("Уютная студия №3", callback_data="sea_comfy3")],
        [InlineKeyboardButton("Уютная студия №4", callback_data="sea_comfy4")],
        [InlineKeyboardButton("← Назад к районам", callback_data="district_back")]
    ])


def sleep_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("2-х комнатная квартира", callback_data="sleep_2rooms")],
        [InlineKeyboardButton("← Назад к районам", callback_data="district_back")]
    ])
