import requests
import re

import random

def generate_sms_code():
    return str(random.randint(100000, 999999))

# sms_code = generate_sms_code()
SMS_EMAIL = "ipu.ntm@bk.ru"
SMS_PASSWORD = 'FM8uRiIG9HJol1FSyMHJYsIXXFa61CtaEBg2DXVE'

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjcxOTAzMDksImlhdCI6MTcyNDU5ODMwOSwicm9sZSI6InVzZXIiLCJzaWduIjoiZmQ0ZmE3NDhiNDc5YzNmZDQ4YzdhYjgzYTU2OGYzY2RiMmFkOTVjNTE1OGJhOTVjMDY0NjU0MjNkYmQ0NGZiMCIsInN1YiI6IjIzNTkifQ.13sR5JIhp_Mvgbf5Q97szj8nCRYcI5ceigr7hN4Lbgo"

def login(email, password):
    URL = "https://notify.eskiz.uz/api/auth/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.request('POST', URL, data=data)
    print(response.json())
    print("status code: ",response.status_code)
    global token
    token = response.json()['data']['token']
    print(token)
    return response


def verify(phone_number, code=None, token=''):
    
    if not token:
        login(SMS_EMAIL, SMS_PASSWORD)
        return verify(phone_number, code)
    token = token
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
        login(SMS_EMAIL, SMS_PASSWORD)
        verify(phone_number, code)
    return response

phone_num = "+998932977419"
code = generate_sms_code()
res = verify(phone_num, code, token=token)
print(res.text)

def get_user_info(token, ):
    URL = "https://notify.eskiz.uz/api/auth/user"
    # URL_BALANCE = "http://notify.eskiz.uz/api/user/get-limit"
    response = requests.request('GET', URL, headers={"Authorization": f"Bearer {token}"})
    balance = response.json()['data']['balance'] # left sms balance
    return response.json()


# print(get_user_info(token))

def get_templates(token):
    URL = "https://notify.eskiz.uz/api/user/templates"
    response = requests.request('GET', URL,  headers={"Authorization": f"Bearer {token}"})
    return response.json()

# print(get_templates(token))




# url = "https://notify.eskiz.uz/api/auth/login"

# payload = {
#     'email': SMS_EMAIL,
#     'password': SMS_PASSWORD
# }

# response = requests.post(url, data=payload)

# if response.status_code == 200:
#     print("Muvaffaqiyatli login!")
#     print(response.json()) 
# else:
#     print(f"Xatolik: {response.status_code}")
#     print(response.text) 