import requests
from urllib.parse import urlencode

# Замените эти значения на ваши данные
client_id = '5fa4e86709494a1872a76745bf66a75cd0'
client_secret = 'c7tv57tg65b7tgn76rf576y67556'

# Получаем от пользователя код, который он получил после авторизации
authorization_code = input("Введите полученный код: ")

# Запрос на получение токена
data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'client_id': client_id,
    'client_secret': client_secret,
}

response = requests.post('https://oauth.yandex.com/token', data=data)

if response.status_code == 200:
    token_data = response.json()
    print("\nПолученный токен:")
    print(token_data['access_token'])
else:
    print(f"Ошибка получения токена: {response.text}")
