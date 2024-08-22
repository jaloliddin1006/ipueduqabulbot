from aiogram import Router, types, F


router = Router()


# @router.message(F.photo)
# async def start_user(message: types.Message):
#     photo = message.photo[-1]
#     await message.answer_photo(photo.file_id, caption=f"{photo.file_id}")
#     await message.answer(message.text)
