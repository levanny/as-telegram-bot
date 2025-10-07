from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import create_async_engine

from app.database.models import DATABASE_URL, Car, SessionLocal
from app.states import CarState

dp = Dispatcher()

engine = create_async_engine(DATABASE_URL, echo=True)

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
    if year <= 1900 or year > 2026:
        await message.answer("გთხოვთ შეიყვანოთ რეალური მანქნანის გამოშვების წელი")
        return
    await state.update_data(year=year)
    await state.set_state(CarState.arrival_time)
    await message.answer("ჩაწერეთ მოყვანის თარიღი:")

# Process arrival time
@dp.message(CarState.arrival_time)
async def process_arrival(message: types.Message, state: FSMContext):
    await state.update_data(arrival_time=message.text)
    await state.set_state(CarState.departure_time)
    await message.answer("ჩაწერეთ გატანების თარიღი:")

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
    if not cleaned_text.isdigit():
        await message.answer("გთხოვთ, ჩაწეროთ მხოლოდ ციფრები მაგალითად: 510 100 500.")
        return
    await state.update_data(phone_number=message.text)
    await message.answer("გთხოვთ ატვირთოთ მანქანის ფოტო 📸")
    await state.set_state(CarState.photo)

@dp.message(CarState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("გთხოვთ ატვირთოთ ფოტო 📸.")
        return
    photo = message.photo[-1]
    await state.update_data(photo_file_id=photo.file_id)

    data = await state.get_data()
    async with SessionLocal() as session:
        new_car = Car(**data)
        session.add(new_car)
        await session.commit()

    await message.answer(
        f"მანქანა წარმატებით დამატებულია!\n"
        f"მოდელი: {data['model']}\n"
        f"წელი: {data['year']}\n"
        f"მოყვანის თარიღი: {data['arrival_time']}\n"
        f"გატანების თარიღი: {data['departure_time']}\n"
        f"საორიენტაციო ფასი: {data['price_range']}\n"
        f"ტელეფონის ნომერი: {data['phone_number']}\n"
        f"ფოტო ატვირთულია ✅"
    )
    await state.clear()