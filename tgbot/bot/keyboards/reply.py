from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📑 Ro'yxatdan o'tish"),
        ],
       
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Ro'yxatdan o'tish uchun bosing",
    selective=True

)

ortga = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

semesterlar = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text="3-semester"),
            KeyboardButton(text="4-semester"),
        ],
        [
            KeyboardButton(text="5-semester"),
            KeyboardButton(text="6-semester"),
        ],
        [
            KeyboardButton(text="7-semester"),
            KeyboardButton(text="8-semester"),
        ],
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

edu_stage = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bakalavr"),
            KeyboardButton(text="O'qishni ko'chirish"),
        ],
   
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)


edu_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kunduzgi"),
            KeyboardButton(text="Sirtqi"),
        ],
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)


register_check = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Tasdiqlash"),
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

maxsus_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="location", request_location=True),
            KeyboardButton(text="contact", request_contact=True),
        ],
        [
            KeyboardButton(text=" poll", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Orqaga")

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

rmk = ReplyKeyboardRemove()
