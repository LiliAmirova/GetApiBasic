import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEME
import allure

BASE_URL = "https://reqres.in/"

LIST_USERS = "api/users?page=2"  # Эндпоинт "Список пользователей"
EMAIL_ENDS = "@reqres.in"  # проверка окончания email  у элемента
AVATAR_ENDS = "-image.jpg"

SINGLE_USER = "api/users/2"
SINGLE_USER_NOT_FOUND = "api/users/23"

DELAYED_REQUEST = "api/users?delay=3" # эндпоинт по таймауту(задержке)

@allure.suite('Проверка запросов данных ВСЕХ пользователей')
@allure.title('Проверяем получение списка пользователей')
def test_list_users():
    with allure.step(f'Делаем запрос по адресу:{BASE_URL + LIST_USERS}'):
        # response = httpx.get("https://reqres.in/api/users?page=2")  Так лучше НЕ писать, т.к. адрес может изм-ся, поэтому url перенести в переменную
        response = httpx.get(BASE_URL + LIST_USERS)
        #rint(response)  # код ответа
        #print(response.text)   # текст запроса

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200 # сравнение полученного статуса кода с ожидаемым

    # print(response.json()['data']) # вывод только блока data
    data = response.json()['data']

    for item in data:   # item -элемент списка
        #r = item['id'])
        with allure.step(f'Проверяем элемент из списка:'):
            validate(item, USER_DATA_SCHEME)           # проверка json-схемы
            with allure.step('Проверяем окончание Email адреса'):
                assert item['email'].endswith(EMAIL_ENDS)  # проверка окончания email
            with allure.step('Проверяем наличие id в ссылке на аватарку'):
                assert  str(item['id']) in item['avatar']   # проверка  наличия номера id в окончании avatar
                assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)  # эта проверка лучше предыдущей -наличия номера id в окончании avatar

#@allure.suite('Проверка запросов данных ОДНОГО пользователей')
@allure.suite('Проверка запросов данных ВСЕХ пользователей')
@allure.title('Проверяем получение данных пользователя')
def test_single_user():
    with allure.step(f'Делаем запрос по адресу:{BASE_URL + SINGLE_USER}'):
        response = httpx.get(BASE_URL + SINGLE_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200  # сравнение полученного статуса кода с ожидаемым
    data = response.json()['data']
    with allure.step('Проверяем окончание Email адреса'):
        assert data['email'].endswith(EMAIL_ENDS)
    with allure.step('Проверяем наличие id в ссылке на аватарку'):
        assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)

#@allure.suite('Проверка запросов на ОТСУТСТВИЕ данных пользователей')
@allure.suite('Проверка запросов данных ВСЕХ пользователей')
@allure.title('Проверяем Отсутствие данных пользователя')
def test_user_not_found():
    with allure.step(f'Делаем запрос по адресу:{BASE_URL + SINGLE_USER_NOT_FOUND}'):
        response = httpx.get(BASE_URL + SINGLE_USER_NOT_FOUND)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404


# # # # # # ТАЙМАУТ
def test_delayed_user_list():
    response = httpx.get(BASE_URL + DELAYED_REQUEST, timeout=3)
    assert response.status_code == 200






