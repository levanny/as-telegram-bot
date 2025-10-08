import calendar
from datetime import date, timedelta
from aiogram import types

def generate_calendar(year:int, month:int):

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)

    keyboard = []
    week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    current_month = date(year, month, 1).strftime("%B %Y")
    keyboard.append([
        types.InlineKeyboardButton(
            text=current_month,
            callback_data="ignore"  # non-clickable
        )
    ])

    keyboard.append([
        types.InlineKeyboardButton(text=day, callback_data="ignore")
    for day in week_days
    ])

    for week in month_days:
        row = []
        for d in week:
            if d.month == month:
                row.append(
                    types.InlineKeyboardButton(
                        text=str(d.day),
                        callback_data=f"pick:{d.isoformat()}"
                    )
                )
            else:
                row.append(types.InlineKeyboardButton(text=" ", callback_data="ignore"))
        keyboard.append(row)

    prev_month = (date(year, month, 15) - timedelta(days=31)).replace(day=1)
    next_month = (date(year, month, 15) + timedelta(days=31)).replace(day=1)

    keyboard.append([
        types.InlineKeyboardButton(text="⬅️", callback_data=f"nav:{prev_month.isoformat()}"),
        types.InlineKeyboardButton(text="➡️", callback_data=f"nav:{next_month.isoformat()}")
    ])

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


