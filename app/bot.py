import asyncio
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv
import logging
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.models import SessionLocal, Car

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# Create bot & dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

class EditCarState(StatesGroup):
    waiting_for_id = State()
    waiting_for_field = State()
    waiting_for_value = State()

class CarState(StatesGroup):
    id = State()
    model = State()
    year = State()
    arrival_time = State()
    departure_time = State()
    price_range = State()
    phone_number = State()

# /help command
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "ხელმისაწვდომი ბრძანებები:\n"
        "/start - ბოტის დაწყება\n"
        "/help - ამ დახმარების შეტყობინების ჩვენება\n"
        "/add_car - ახალი მანქანის დამატება\n"
        "/list - ბაზაში არსებული მანქანების ჩამოთვლა\n"
        "ან კითხეთ შეკითხვები, მაგალითად:\n"
        "- ჩემი შემდეგი სერვისი როდის არის?\n"
        "- სერვისის ღირებულება რამდენია?\n"
        "- რა უნდა გამოასწორონ?"
    )

# /start command
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("გამარჯობა! მე ვარ შენი ბოტი 🚀")

# /add_car command
@dp.message(Command("add_car"))
async def cmd_add_car(message: types.Message, state: FSMContext):
    await message.answer("ჩაწერეთ მანქანის მოდელი:")
    await state.set_state(CarState.model)

# Process car model
@dp.message(CarState.model)
async def process_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await state.set_state(CarState.year)
    await message.answer("ჩაწერეთ მანქანის გამოშვების წელი:")

# Process car year
@dp.message(CarState.year)
async def process_year(message: types.Message, state: FSMContext):
    try:
        year = int(message.text)
    except ValueError:
        await message.answer("გთხოვთ, ჩაწეროთ მხოლოდ გამოშვების წლის რიცხვი, მაგალითად - 2025.")
        return
    await state.update_data(year=year)
    await state.set_state(CarState.arrival_time)
    await message.answer("ჩაწერეთ მოსვლის დრო:")

# Process arrival time
@dp.message(CarState.arrival_time)
async def process_arrival(message: types.Message, state: FSMContext):
    await state.update_data(arrival_time=message.text)
    await state.set_state(CarState.departure_time)
    await message.answer("ჩაწერეთ გასვლის დრო:")

# Process departure time
@dp.message(CarState.departure_time)
async def process_departure(message: types.Message, state: FSMContext):
    await state.update_data(departure_time=message.text)
    await state.set_state(CarState.price_range)
    await message.answer("ჩაწერეთ ფასის დიაპაზონი:")

# Process price range
@dp.message(CarState.price_range)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price_range=message.text)
    await state.set_state(CarState.phone_number)
    await message.answer("ჩაწერეთ საკონტაქტო ტელეფონის ნომერი: +995")

# Process phone number and save to DB
@dp.message(CarState.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    cleaned_text = message.text.replace(" ", "")

    # Keep asking until valid
    if not cleaned_text.isdigit():
        await message.answer("გთხოვთ, ჩაწეროთ მხოლოდ ციფრები მაგალითად: 510 100 500.")
        return

    data = await state.get_data()
    data["phone_number"] = message.text

    # Save to DB
    async with SessionLocal() as session:
        new_car = Car(**data)
        session.add(new_car)
        await session.commit()

    await message.answer(
        f"მანქანა წარმატებით დამატებულია!\n"
        f"მოდელი: {data['model']}\n"
        f"წელი: {data['year']}\n"
        f"მოსვლა: {data['arrival_time']}\n"
        f"გასვლა: {data['departure_time']}\n"
        f"ფასი: {data['price_range']}\n"
        f"ტელეფონი: {data['phone_number']}"
    )
    await state.clear()

# List all cars
@dp.message(Command("list"))
async def list_cars(message: types.Message):
    async with SessionLocal() as session:
        result = await session.execute(select(Car))
        cars = result.scalars().all()

    if not cars:
        await message.answer("მანქანები ჯერ არ დამატებულა!")
        return

    reply = ""
    for car in cars:
        reply += (
            f"ID: {car.id}\n"
            f"მოდელი: {car.model}\n"
            f"წელი: {car.year}\n"
            f"მოსვლა: {car.arrival_time}\n"
            f"გასვლა: {car.departure_time}\n"
            f"ფასი: {car.price_range}\n"
            f"ტელეფონი: {car.phone_number}\n"
            "--------------------\n"
        )

    await message.answer(reply)

# /edit command
@dp.message(Command("edit"))
async def cmd_edit(message: types.Message, state: FSMContext):
    await message.answer("ჩაწერეთ იმ მანქანის ID, რომლის შეცვლაც გსურთ:")
    await state.set_state(EditCarState.waiting_for_id)

@dp.message(EditCarState.waiting_for_id)
async def edit_get_id(message: types.Message, state:FSMContext):
    try:
        car_id = int(message.text)
    except ValueError:
        await message.answer("❌ გთხოვთ, ჩაწეროთ მხოლოდ რიცხვი (მაგალითად: 2).")
        return

    async with SessionLocal() as session:
        result = await session.execute(select(Car).where(Car.id == car_id))
        car = result.scalar_one_or_none()

    if not car:
        await message.answer("❌ მანქანა ვერ მოიძებნა ამ ID-ით.")
        await state.clear()
        return

    await state.update_data(car_id=car_id)
    await message.answer(
        "რომელი ველის შეცვლა გსურთ?\n"
        "აირჩიეთ: model, year, arrival_time, departure_time, price_range, phone_number"
    )
    await state.set_state(EditCarState.waiting_for_field)


# Step 2: get field name
@dp.message(EditCarState.waiting_for_field)
async def edit_get_field(message: types.Message, state: FSMContext):
    field = message.text.strip()
    valid_fields = {"model", "year", "arrival_time", "departure_time", "price_range", "phone_number"}

    if field not in valid_fields:
        await message.answer("❌ ველი არასწორია. სცადეთ თავიდან.")
        return

    await state.update_data(field=field)
    await message.answer(f"ჩაწერეთ ახალი მნიშვნელობა ველისთვის: {field}")
    await state.set_state(EditCarState.waiting_for_value)

# Step 3: save new value
@dp.message(EditCarState.waiting_for_value)
async def edit_save_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    car_id = data["car_id"]
    field = data["field"]
    new_value = message.text.strip()

    # numeric fields -> cast to int
    if field in {"year"}:
        try:
            new_value = int(new_value)
        except ValueError:
            await message.answer("❌ ეს ველი უნდა იყოს რიცხვი.")
            await state.clear()
            return

    async with SessionLocal() as session:
        result = await session.execute(select(Car).where(Car.id == car_id))
        car = result.scalar_one_or_none()

        if not car:
            await message.answer("მანქანა ვერ მოიძებნა ბაზაში!")
            await state.clear()
            return

        setattr(car, field, new_value)
        await session.commit()

# Run the bot
async def main():
    print("ბოტი იწყება...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
