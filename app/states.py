from aiogram.fsm.state import State, StatesGroup

class DateRange(StatesGroup):
    picking_start = State()
    picking_end = State()

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
    photo = State()
    photo_choice = State()

class DeleteCarState(StatesGroup):
    waiting_for_id = State()