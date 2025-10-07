from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select

from database.models import Car, SessionLocal

router = Router()


# List all cars
@router.message(Command("list"))
async def list_cars(message: types.Message):
    async with SessionLocal() as session:
        result = await session.execute(select(Car))
        cars = result.scalars().all()

    if not cars:
        await message.answer("მანქანები ჯერ არ დამატებულა!")
        return

    for car in cars:
        car_info = (
            f"ID: {car.id}\n"
            f"მოდელი: {car.model}\n"
            f"წელი: {car.year}\n"
            f"მოყვანის თარიღი: {car.arrival_time}\n"
            f"გატანების თარიღი: {car.departure_time}\n"
            f"საორიენტაციო ფასი: {car.price_range}\n"
            f"ტელეფონის ნომერი: {car.phone_number}\n"
            "--------------------\n"
        )

        if car.photo_file_id:
            await message.answer_photo(photo=car.photo_file_id, caption=car_info)
        else:
            await message.answer(car_info)