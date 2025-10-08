from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from database.models import Car, SessionLocal
from app.states import EditCarState

router = Router()



@router.message(Command("edit"))
async def cmd_edit(message: types.Message, state: FSMContext):
    await message.answer("ჩაწერეთ იმ მანქანის ID, რომლის შეცვლაც გსურთ:")
    await state.set_state(EditCarState.waiting_for_id)

@router.message(EditCarState.waiting_for_id)
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
@router.message(EditCarState.waiting_for_field)
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
@router.message(EditCarState.waiting_for_value)
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
