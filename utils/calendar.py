from datetime import date, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_calendar(year: int, month: int, min_date: date = None):
    keyboard = []
    month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                   "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    keyboard.append([InlineKeyboardButton(
        f"{month_names[month - 1]} {year}",
        callback_data="ignore"
    )])

    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard.append([InlineKeyboardButton(day, callback_data="ignore") for day in week_days])

    first_day = date(year, month, 1)
    start_weekday = first_day.weekday()

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    days_in_month = (next_month - first_day).days

    week = []
    for _ in range(start_weekday):
        week.append(InlineKeyboardButton(" ", callback_data="ignore"))

    for day_num in range(1, days_in_month + 1):
        current_date = date(year, month, day_num)

        if min_date and current_date < min_date:
            button_text = "❌"
            callback = "ignore"
        else:
            button_text = str(day_num)
            callback = f"cal_day_{year}_{month}_{day_num}"

        week.append(InlineKeyboardButton(button_text, callback_data=callback))

        if len(week) == 7:
            keyboard.append(week)
            week = []

    if week:
        keyboard.append(week)

    nav_buttons = []
    prev_month = date(year, month, 1) - timedelta(days=1)
    prev_month = date(prev_month.year, prev_month.month, 1)
    nav_buttons.append(InlineKeyboardButton("◀️", callback_data=f"cal_prev_{prev_month.year}_{prev_month.month}"))

    next_month_date = date(year, month, 1) + timedelta(days=days_in_month)
    if next_month_date.month == month:
        if month == 12:
            next_month_date = date(year + 1, 1, 1)
        else:
            next_month_date = date(year, month + 1, 1)
    nav_buttons.append(
        InlineKeyboardButton("▶️", callback_data=f"cal_next_{next_month_date.year}_{next_month_date.month}"))
    keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(keyboard)