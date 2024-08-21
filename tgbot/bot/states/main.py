from aiogram.filters.state import State, StatesGroup


class MessageState(StatesGroup):
    message = State()
    check = State()
    
    
class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()
    phone_number = State()
    passport = State()
    birthday = State()
    edu_stage = State()
    edu_type = State()
    speciality = State()
    transfer_image = State()
    semester = State()
    check = State()