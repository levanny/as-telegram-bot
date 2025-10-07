import asyncio
import logging
from aiogram import Bot, Dispatcher, Router

from app.config import BOT_TOKEN
from app.handlers import help_car, add_car, edit_car, list_car

logging.basicConfig(level=logging.INFO)

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()



dp.include_router(add_car.router)
dp.include_router(list_car.router)
dp.include_router(edit_car.router)

async def main():
    print("🤖 Bot is starting...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())