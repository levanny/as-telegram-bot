from app.states import DeleteCarState
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, delete

from database.models import Car, SessionLocal

router = Router()


@router.message(Command("delete"))
async def cmd_delete(message: types.Message, state: FSMContext):
    await message.answer("ჩაწერეთ იმ მანქანის ID, რომლის წაშლაც გსურთ:")
    await state.set_state(DeleteCarState.waiting_for_id)

@router.message(DeleteCarState.waiting_for_id)
async def delete_car_by_id(message: types.Message, state: FSMContext):
    try:
        car_id = int(message.text)
    except ValueError:
        await message.answer("❌ გთხოვთ ჩაწეროთ მხოლოდ რიცხვი (მაგალითად: 2).")
        return

    async with SessionLocal() as session:
        result = await session.execute(select(Car).where(Car.id == car_id))
        car = result.scalar_one_or_none()

        if not car:
            await message.answer("❌ მანქანა ვერ მოიძებნა ამ ID-ით.")
            await state.clear()
            return

        await session.execute(delete(Car).where(Car.id == car_id))
        await session.commit()

    await message.answer(f"✅ მანქანა ID {car_id} წარმატებით წაიშალა.")
    await state.clear()
