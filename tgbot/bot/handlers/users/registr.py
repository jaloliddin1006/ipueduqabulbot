from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from docx2pdf import convert
from docxtpl import DocxTemplate
from src.settings import BASE_URL_CONTRACT
from tgbot.bot.loader import bot
from tgbot.bot.keyboards import reply, builders
from tgbot.models import User, Speciality, Contract
from tgbot.bot.states.main import RegisterState
import re, os
from django.conf import settings
from tgbot.utils import IntegerPronunciation
from datetime import datetime
import subprocess

PASSPORT_REGEX = re.compile(r"^[A-Z]{2}\d{7}$")
PHONE_REGEX1 = re.compile(r"^\+998\d{9}$")
PHONE_REGEX2 = re.compile(r"^998\d{9}$")
PHONE_REGEX3 = re.compile(r"^\d{9}$")
BIRTHDAY_REGEX = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")


router = Router()

@router.message(F.text == "Orqaga")
async def back_func(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Ro'yxatdan o'tish bekor qilindi. \n\nRo'yxatdan o'tish uchun bosing", reply_markup=reply.main)


@router.message(F.text == "📑 Ro'yxatdan o'tish")
async def get_first_name_func(message: types.Message, state: FSMContext):
    
        
    await state.set_state(RegisterState.first_name)
    await message.answer("Ismingizni kiriting:", reply_markup=reply.ortga)
    
@router.message(RegisterState.first_name, F.text)
async def get_last_name_func(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegisterState.last_name)
    await message.answer("Familiyangizni kiriting:", reply_markup=reply.ortga)
    
@router.message(RegisterState.last_name, F.text)
async def get_middle_name_func(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegisterState.middle_name)
    await message.answer("Otangizning ismini kiriting:", reply_markup=reply.ortga)
    
@router.message(RegisterState.middle_name, F.text)
async def get_phone_number_func(message: types.Message, state: FSMContext):
    await state.update_data(middle_name=message.text)
    await state.set_state(RegisterState.phone_number)
    await message.answer("Telefon raqamingizni kiriting: \n\nNamuna: <code> +998932977419</code> ", reply_markup=reply.ortga)
    
@router.message(RegisterState.phone_number, F.text)
async def get_passport_func(message: types.Message, state: FSMContext):
    if not PHONE_REGEX1.match(message.text) and not PHONE_REGEX2.match(message.text) and not PHONE_REGEX3.match(message.text):
        await message.answer("Telefon raqamingizni noto'g'ri kiritdingiz. Iltimos qaytadan kiriting. \n\nNamuna: <code> +998932977419</code>", reply_markup=reply.ortga)
        return
    await state.update_data(phone_number=message.text)
    await state.set_state(RegisterState.passport)
    await message.answer("Pasportingizni kiriting:\n\nNamuna: <code>AB1234567</code>", reply_markup=reply.ortga)
    
@router.message(RegisterState.passport, F.text)
async def get_edu_stage_func(message: types.Message, state: FSMContext):
    passport = message.text
    if not PASSPORT_REGEX.match(passport):
        await message.answer("Pasportingizni noto'g'ri kiritdingiz. Iltimos qaytadan kiriting. \n\nNamuna: <code>AB1234567</code>", reply_markup=reply.ortga)
        return
    await state.update_data(passport=passport)
    await state.set_state(RegisterState.birthday)
    await message.answer("Tug'ilgan kuningizni kiriting:\n\nNamuna: <code>15.09.1999</code>", reply_markup=reply.ortga)
    
@router.message(RegisterState.birthday, F.text)
async def get_edu_stage_func(message: types.Message, state: FSMContext):
    birthday = message.text
    if not BIRTHDAY_REGEX.match(birthday):
        await message.answer("Tug'ilgan kuningizni noto'g'ri kiritdingiz. Iltimos qaytadan kiriting. \n\nNamuna: <code>15.09.1999</code>", reply_markup=reply.ortga)
        return
    await state.update_data(birthday=birthday)
    await state.set_state(RegisterState.edu_stage)
    await message.answer("O'qish darajangizni tanlang:", reply_markup=reply.edu_stage)
    
    
@router.message(RegisterState.edu_stage, F.text)
async def get_edu_type_func(message: types.Message, state: FSMContext):
    if message.text not in ["Bakalavr", "O'qishni ko'chirish"]:
        await message.answer("Iltimos, tanlangan variantlar orasidan tanlang", reply_markup=reply.edu_stage)
        return
    
    # if message.text == "O'qishni ko'chirish":
    #     await state.update_data(edu_stage="O'qishni ko'chirish")
    #     await state.set_state(RegisterState.edu_type)
    #     await message.answer("Ta'lim turini tanlang:", reply_markup=reply.edu_type)
    #     return
    await state.update_data(edu_stage=message.text)
    await state.set_state(RegisterState.edu_type)
    await message.answer("Ta'lim turini tanlang:", reply_markup=reply.edu_type)
    
    
@router.message(RegisterState.edu_type, F.text)
async def get_speciality_func(message: types.Message, state: FSMContext):
    if message.text not in ["Kunduzgi", "Sirtqi"]:
        await message.answer("Iltimos, tanlangan variantlar orasidan tanlang", reply_markup=reply.edu_type)
        return
    await state.update_data(edu_type=message.text,
                            is_internal=message.text == "Kunduzgi",
                            is_external=message.text == "Sirtqi"
                            )

    await state.set_state(RegisterState.speciality)

    if message.text == "Kunduzgi":
        speciality_names = await sync_to_async(list)(
            Speciality.objects.filter(is_internal=True).values_list('name', flat=True)
        )
    else:
        speciality_names = await sync_to_async(list)(
            Speciality.objects.filter(is_external=True).values_list('name', flat=True)
        )

    await message.answer("Muttaxasislik yo'nalishini tanlang tanlang:", reply_markup=await builders.build_speciality_kb(speciality_names))
  

def get_state_data(data):
    return (
        f"<b>Ism:</b> {data.get('first_name')}\n"
        f"<b>Familiya:</b> {data.get('last_name')}\n"
        f"<b>Otasining ismi:</b> {data.get('middle_name')}\n"
        f"<b>Telefon raqami:</b> {data.get('phone_number')}\n"
        f"<b>Pasport:</b> {data.get('passport')}\n"
        f"<b>Tug'ilgan kun:</b> {data.get('birthday')}\n"
        f"<b>O'qish darajasi:</b> {data.get('edu_stage')}\n"
        f"<b>Ta'lim turi:</b> {data.get('edu_type')}\n"
        f"<b>Specializatsiya:</b> {data.get('speciality_name')}\n"
    )
      
@router.message(RegisterState.speciality, F.text)
async def get_semester_func(message: types.Message, state: FSMContext):
    speciality_name = message.text
    try:
        speciality = await sync_to_async(Speciality.objects.get)(name=speciality_name)
    except Speciality.DoesNotExist:
        await message.answer("Iltimos, ko'rsatilgan yo'nalishlardan birini tanlang", reply_markup=builders.build_speciality_kb())
        return
    
    
    await state.update_data(speciality_id=speciality.id, 
                            speciality_name=speciality_name,
                           )
    data = await state.get_data()
    if data.get("edu_stage") == "O'qishni ko'chirish":
        await state.set_state(RegisterState.transfer_image)
        await message.answer("Trnskript rasmini yuboring", reply_markup=reply.ortga)
        return
    text = get_state_data(data)
    await message.answer(text, parse_mode=ParseMode.HTML)
    await state.set_state(RegisterState.check)
    await message.answer("Ma'lumotlaringizni tekshiring", reply_markup=reply.register_check)
    
    
@router.message(RegisterState.transfer_image, F.photo)
async def get_semester_func(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    
    os.makedirs("media/transkrips", exist_ok=True)
    
    destination = 'media/transkrips/' + file_info.file_path.split('/')[-1]
    with open(destination, 'wb') as new_file:
        new_file.write(downloaded_file.read())
        
    await state.update_data(transfer_image=destination, transfer_image_id=file_id)
    await state.set_state(RegisterState.semester)
    await message.answer("Semestrni tanlang:", reply_markup=builders.get_semester())
    
    
@router.message(RegisterState.transfer_image, ~F.photo)
async def get_semester_func(message: types.Message, state: FSMContext):
    await message.answer("Trnskript rasmini yuboring", reply_markup=reply.ortga)
    return

@router.message(RegisterState.semester, F.text)
async def get_check_func(message: types.Message, state: FSMContext):
    if message.text not in [str(i) for i in range(3, 9)]:
        await message.answer("Iltimos, tanlangan variantlar orasidan tanlang", reply_markup=builders.get_semester())
        return
    await state.update_data(semester=message.text)
    
    data = await state.get_data()
    text = get_state_data(data)
    text += f"<b>Semestr:</b> {data.get('semester')}\n"
    await message.answer_photo(photo=data.get('transfer_image_id'), caption=text, parse_mode=ParseMode.HTML)
    await state.set_state(RegisterState.check)
    await message.answer("Ma'lumotlaringizni tekshiring", reply_markup=reply.register_check)
    


def generate_pdf(doc_path, path):

    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])
    return doc_path

@router.message(RegisterState.check, F.text == "✅ Tasdiqlash")
async def get_check_func(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    contract = await sync_to_async(Contract.objects.create)(
        user=user,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        middle_name=data.get('middle_name'),
        phone_number=data.get('phone_number'),
        passport=data.get('passport'),
        birthday = data.get('birthday'),
        edu_stage=data.get('edu_stage'),
        is_internal=data.get('is_internal'),
        is_external=data.get('is_external'),
        speciality_id=data.get('speciality_id'),
        transkrip=data.get('transfer_image', None),
        semester=data.get('semester', 1),
    )
    
    
    if data.get("edu_stage") == "O'qishni ko'chirish":
        await message.answer("Sizning ma'lumotlaringiz qabul qilindi.", reply_markup=reply.main)
        return
        
    
    speciality = await sync_to_async(Speciality.objects.get)(id=data.get('speciality_id'))

    # Generate DOCX file
    doc_path = os.path.join(settings.BASE_DIR, "contract.docx")
    doc = DocxTemplate(doc_path)
    contract_id = contract.id
    price = speciality.get_contract_price(data.get('is_internal'))
    full_name = f"{data.get('first_name')} {data.get('last_name')} {data.get('middle_name')}"
    context = {
        "contract_id": contract_id,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "full_name": full_name,
        "edu_stage": data.get('edu_stage'),
        "speciality": data.get('speciality_name'),
        "period": speciality.get_periot(data.get('is_internal')),
        "edu_type": contract.edu_type,
        "contract_summ": price,
        "contract_alpha": IntegerPronunciation().main(price),
        "birthday": contract.birthday,
        "passport": contract.passport,
        "phone_number": contract.phone_number,
    }

    doc.render(context)

    # Create the directory if it doesn't exist
    os.makedirs("media/contract", exist_ok=True)
    file_base_path = f"media/contract/{contract_id}-contract"
    # Save the DOCX file
    docx_path = os.path.join(settings.BASE_DIR, f"{file_base_path}.docx")
    print(docx_path)
    doc.save(docx_path)

    # Convert DOCX to PDF using LibreOffice
    pdf_path = os.path.join(settings.BASE_DIR, f"{file_base_path}.pdf")
    # try:
    #     convert(docx_path, pdf_path)
    # except Exception as e:
    generate_pdf(docx_path, os.path.join(settings.BASE_DIR, f"media/contract"))
    # subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', 'media/contract', docx_path.replace("media/contract/", "")])
    # except Exception as e:
    #     print("error:           ",e)
        
    contract.contract = f"contract/{contract_id}-contract.pdf"
    await sync_to_async(contract.save)()
    
    await state.clear()
    await message.answer("Sizning ma'lumotlaringiz qabul qilindi.")
    # await message.answer(f"[📂 Yuklab olish | Contract]({BASE_URL_CONTRACT}{file_base_path}.pdf)", reply_markup=reply.main, parse_mode=ParseMode.MARKDOWN)
    
    pdf_file = FSInputFile(pdf_path)
    await message.answer_document(pdf_file, caption="Sizning shartnomangiz tayyor. Yuklab oling.")
  


context = {
    "contract_id":8222,
    "date":"2021-09-15",
    "full_name":"Abdulloh Xabibullaev Abdulloevich",
    "edu_stage":"Bakalavr",
    "speciality":"Pedagogika va psixologiya",
    "period":4,
    "edu_type":"Kunduzgi",
    "contract_summ":12000000,
    "contract_alpha":"O'n ikki million",
    "birthday":"15-09-1999",
    "passport":"AA1234567",
    "phone_number":"+998932977419",
    
}

