import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# Create bot & dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

#/start command
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Hello! 👋 I am your Car Service Bot.\n"
        "You can ask me about your car's status or use /help to see commands."
    )

#/help command
@dp.message(Command("help"))
async def help_command(message:types.Message):
    await message.answer(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "Or ask questions like:\n"
        "- When is my next service?\n"
        "- What is the service cost?\n"
        "- What needs to be repaired?"
    )




# Respond to any message
@dp.message()
async def any_message(message: types.Message):
    logging.info(f"Received message: {message.text} from {message.from_user.id}")
    reply = "Hello 👋"
    logging.info(f"Replying to {message.from_user.id}: {reply}")
    await message.answer(reply)

# /start command handler
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Hello! I'm your bot 🚀")

async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
