from aiogram.filters import Command
from aiogram import types, Router

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "ხელმისაწვდომი ბრძანებები:\n"
        "/help - დამხმარე შეტყობინების ჩვენება\n"
        "/add - ახალი მანქანის დამატება\n"
        "/list - ბაზაში არსებული მანქანების ჩამოთვლა\n"
        "/edit - ბაზაში მანქანის მონაცემების შეცვლა\n"
        "/delete - ბაზაში რომელიმე მანქანის წაშლა\n"
    )