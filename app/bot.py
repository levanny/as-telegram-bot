import asyncio
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv
import logging
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import SessionLocal, engine, Base
from database.models import Car

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# Create bot & dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

class CarState(StatesGroup):
    model = State()
    year = State()
    arrival_time = State()
    departure_time = State()
    price_range = State()
    phone_number = State()

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

@dp.message(Command("add_car"))
async def cmd_add_car(message: types.Message, state: FSMContext):
    await message.answer("Enter car model:")
    await state.set_state(CarState.model)

@dp.message(CarState.model)
async def process_model(message: types.Message, state: FSMContext):
    try:
        year = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid number for the year.")
        return
    await state.update_data(year=year)
    await message.answer("Enter car year:")
    await state.set_state(CarState.year)

@dp.message(CarState.year)
async def process_year(message: types.Message, state: FSMContext):
    await state.update_data(year=int(message.text))
    await message.answer("Enter arrival time:")
    await state.set_state(CarState.arrival_time)

@dp.message(CarState.arrival_time)
async def process_arrival(message: types.Message, state: FSMContext):
    await state.update_data(arrival_time=int(message.text))
    await message.answer("Enter departure time:")
    await state.set_state(CarState.departure_time)

@dp.message(CarState.departure_time)
async def process_departure(message: types.Message, state: FSMContext):
    await state.update_data(departure_time=int(message.text))
    await message.answer("Enter price range:")
    await state.set_state(CarState.price_range)

@dp.message(CarState.price_range)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price_range=message.text)
    await message.answer("Enter contact phone number:")
    await state.set_state(CarState.phone_number)

@dp.message(CarState.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data["phone_number"] = message.text

    # Save to DB
    async with SessionLocal() as session:
        new_car = Car(**data)
        session.add(new_car)
        await session.commit()

    await message.answer(f"Car added successfully!\nModel: {data['model']}, Year: {data['year']}")
    await state.clear()

if __name__ == "__main__":
    asyncio.run(main())
