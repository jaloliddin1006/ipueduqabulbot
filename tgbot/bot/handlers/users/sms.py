from tgbot.models import SMSToken, SMSConfirmation
from django.conf import settings
from asgiref.sync import sync_to_async
import requests
import re
import random




async def login(email, password):
    URL = "https://notify.eskiz.uz/api/auth/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.request('POST', URL, data=data)
    # SMSToken.objects.create(token=response.json()['data']['token'])
    res_token = response.json()['data']['token']
    await sync_to_async(SMSToken.objects.create)(token=res_token)
    return response


async def verify(phone_number, code):
    # token_obj = SMSToken.objects.last()
    token_obj = await sync_to_async(SMSToken.objects.last)()
    if not token_obj:
        await login(settings.SMS_EMAIL, settings.SMS_PASSWORD)
        return await verify(phone_number, code)
    
    token = token_obj.token
    phone_number = re.sub(r'\D', '', phone_number)
    URL = "https://notify.eskiz.uz/api/message/sms/send"
    PARAMS = {
        "Authorization": f"Bearer {token}"
    }
    
    message = f"Sizning https://t.me/ipueduqabulbot orqali to'lov shartnomasini olish uchun tasdiqlash kodingiz: {code}"

    data = {
        'mobile_phone': phone_number,
        'message': message,
        'from': 'IPU',
        'callback_url': 'http://0000.uz/test.php'
    }
    response = requests.request('POST', URL, data=data, headers=PARAMS)
    if response.status_code == 401:
        await login(settings.SMS_EMAIL, settings.SMS_PASSWORD)
        await verify(phone_number, code)
    return response.json()




async def generate_sms_code(telegram_id, phone_number):
    
    code = '000000'
    result = {"id":"f7628c82-3ab9-471a-966b-dd5c9f4ed27e","message":"Waiting for SMS provider","status":"waiting"}
    if settings.IS_SEND_SMS:
        code = str(random.randint(100000, 999999))
        result = await verify(phone_number, code)
        if result.get('status') == "error":
            return result
    # SMSConfirmation.objects.create(telegram_id=telegram_id, phone_number=phone_number, code=code)
    await sync_to_async(SMSConfirmation.objects.create)(telegram_id=telegram_id, phone_number=phone_number, code=code)
    return result