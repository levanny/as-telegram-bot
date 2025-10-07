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


# /calendar that later will be integrated into /add 's choosing date part
'''
# @router.message(Command("calendar"))
@dp.message(Command("calendar"))
async def start_calendar(message: types.Message, state:FSMContext):
    today = date.today()
    await message.answer("აირჩიეთ მოყვანის თარიღი:",
                         reply_markup=generate_calendar(today.year, today.month))
    await state.set_state(DateRange.picking_start)

#Handle date clicks
@dp.callback_query(F.data.startswith("pick:"))
async def handle_date(callback: types.CallbackQuery, state: FSMContext):
    picked = date.fromisoformat(callback.data.split(":")[1])
    current_state = await state.get_state()
    if current_state == DateRange.picking_start:
        await state.update_data(start=picked.isoformat())
        await callback.message.edit_text(
            f"მოყვანის თარიღი არჩეულია: {picked}\nაირჩიეთ წაყვანის თარიღი:",
            reply_markup=generate_calendar(picked.year, picked.month)
        )
        await state.set_state(DateRange.picking_end)

    elif current_state == DateRange.picking_end:
        await state.update_data(end=picked.isoformat())
        data = await state.get_data()

        start_date = date.fromisoformat(data['start'])
        end_date = date.fromisoformat(data['end'])
        if data['start'] > data['end']:
            temp = end_date
            end_date = start_date
            start_date = temp
        await callback.message.edit_text(
            f"შენ აირჩიე დიაპაზონი:\n{start_date} ➝ {end_date}"
        )
        await state.clear()

    await callback.answer()

#Handle navigation
@dp.callback_query(F.data.startswith("nav:"))
async def handle_nav(callback: types.CallbackQuery):
    new_month = date.fromisoformat(callback.data.split(":")[1])
    today = date.today()

    # limit to current month + 3 months
    if new_month < today.replace(day=1) or new_month >(today.replace(day=1) + timedelta(days=90)):
        await callback.answer("ვიზიტის ჩანიშვნის ლიმიტი მხოლოდ მომდევნო 3 თვეა.")
        return
    await callback.message.edit_reply_markup(
        reply_markup=generate_calendar(new_month.year, new_month.month)
    )
    await callback.answer()

'''
