from aiogram.filters import Command
from aiogram import types, Dispatcher

dp = Dispatcher()

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "ხელმისაწვდომი ბრძანებები:\n"
        "/start - ბოტის დაწყება\n"
        "/help - ამ დახმარების შეტყობინების ჩვენება\n"
        "/add_car - ახალი მანქანის დამატება\n"
        "/list - ბაზაში არსებული მანქანების ჩამოთვლა\n"
        "/edit_car - რათა შეცვალოთ მანქანის ნებისმიერი მონაცემი\n"
    )