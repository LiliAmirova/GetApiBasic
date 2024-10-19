import json
import httpx
import pytest
import allure

from jsonschema import validate
from core.contracts import REGISTERED_USER_SCHEME
from core.contracts import LOGIN_USER_SCHEME

BASE_URL = "https://reqres.in/"
REGISTER_USER = "api/register"
LOGIN_USER = "api/login"

# открываем и читаем файл в паролями
json_file = open('C:/Users/Пользователь/PycharmProjects/RequestGET/core/new_users_data.json')

# загрузить файл
users_data = json.load(json_file)
#print(users_data)

@allure.suite('5_Register - successful')
@allure.title('Проверяем Register - successful')
@pytest.mark.parametrize('users_data', users_data)
def test_successful_register(users_data):
    headers = {'Content-Type': 'application/json'}      # Заголовки и передача заголовков
    with allure.step(f'Отправляем запрос по адресу: {BASE_URL + REGISTER_USER}'):
        response = httpx.post(BASE_URL + REGISTER_USER, json=users_data, headers=headers)
        #print(users_data)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200
    with allure.step(f'Проверяем валидацию схемы'):
        validate(response.json(), REGISTERED_USER_SCHEME)

@allure.suite('6_Register - unsuccessful')
@allure.title('Проверяем Register - unsuccessful')
def test_unsuccessful_register():
    body = {
    "email": "sydney@fife"
    }
    with allure.step(f'Отправляем запрос по адресу: {BASE_URL + REGISTER_USER}'):
        response = httpx.post(BASE_URL + REGISTER_USER, json=body)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 400

@allure.suite('7_Login - successful')
@allure.title('Проверяем Login - successful')
@pytest.mark.parametrize('users_data', users_data)
def test_successful_login(users_data):
    with allure.step(f'Отправляем запрос по адресу: {BASE_URL + LOGIN_USER}'):
        response = httpx.post(BASE_URL + LOGIN_USER, json=users_data)
    #print(users_data)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200
    with allure.step(f'Проверяем валидацию схемы'):
        validate(response.json(), LOGIN_USER_SCHEME)


@allure.suite('8_Login - unsuccessful')
@allure.title('Проверяем Login - unsuccessful')
def test_unsuccessful_login():
    body = {
    "email": "sydney@fife"
    }
    with allure.step(f'Отправляем запрос по адресу: {BASE_URL + REGISTER_USER}'):
        response = httpx.post(BASE_URL + REGISTER_USER, json=body)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 400

