import httpx
from jsonschema import validate
from core.contracts import CREATE_USER_SCHEME
from core.contracts import UPDATE_USER_SCHEME
import datetime
import allure

BASE_URL = "https://reqres.in/"
CREATE_USER = "api/users"
UPDATE_USER = "api/users/2"

@allure.suite('1_Проверка запроса CREATE')
@allure.title('Проверяем запрос CREATE c полями: "name" и "job"')
def test_create_user_with_name_and_job():
    body = {  # Это словарь
        "name": "morpheus",
        "job": "leader"
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + CREATE_USER}'):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)
        #print(response.json())
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 201  # проверка код ответа

    response_json = response.json()
    creation_date = response_json['createdAt'].replace('T',' ')  # получение даты создания и возвращается строка
    current_date = str(datetime.datetime.utcnow()) # получение текущей даты для сравнения (import datetime) и приведение к типу строка
    with allure.step(f'Проверяем созданный элемент: {response_json['id']}'):
        validate(response_json, CREATE_USER_SCHEME)  # валидация json схемы

    with allure.step(f'Проверяем "name"'):
        # response полученный(слева) сравниваем с response отправленным (справа)
        assert response_json['name'] == body['name']

    with allure.step(f'Проверяем "job"'):
        assert response_json['job'] == body['job']
    #print(creation_date[0:16])
    #print(current_date[0:16])
    with allure.step(f'Проверяем "createdAt"'):
        assert creation_date[0:16] == current_date[0:16] # отрезаем время до минут (т.е 15 символов, но диапазон не отражает символ в последней границе, поэтому +1 в диапазоне


@allure.suite('1_Проверка запроса CREATE')
@allure.title('Проверяем запрос CREATE без поля: "name"')
def test_create_user_without_name(): # без "name"
    body = {
        "job": "leader"
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + CREATE_USER}'):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 201  # проверка код ответа

    response_json = response.json()
    creation_date = response_json['createdAt'].replace('T',' ')  # получение даты создания и возвращается строка
    current_date = str(datetime.datetime.utcnow()) # получение текущей даты для сравнения (import datetime) и приведение к типу строка
    with allure.step(f'Проверяем созданный элемент: {response_json['id']}'):
        validate(response_json, CREATE_USER_SCHEME)  # валидация json схемы
    with allure.step(f'Проверяем "job"'):
        assert response_json['job'] == body['job']
    with allure.step(f'Проверяем "createdAt"'):
        assert creation_date[0:16] == current_date[0:16] # отрезаем время до минут (т.е 15 символов, но диапазон не отражает символ в последней границе, поэтому +1 в диапазоне


@allure.suite('1_Проверка запроса CREATE')
@allure.title('Проверяем запрос CREATE без поля: "job"')
def test_create_user_without_job():
    body = {
        "name": "morpheus"
    }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + CREATE_USER}'):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 201  # проверка код ответа

    response_json = response.json()
    creation_date = response_json['createdAt'].replace('T',' ')  # получение даты создания и возвращается строка
    current_date = str(datetime.datetime.utcnow()) # получение текущей даты для сравнения (import datetime) и приведение к типу строка
    with allure.step(f'Проверяем созданный элемент: {response_json['id']}'):
        validate(response_json, CREATE_USER_SCHEME)  # валидация json схемы
    with allure.step(f'Проверяем "name"'):
        assert response_json['name'] == body['name']
    with allure.step(f'Проверяем "createdAt"'):
        assert creation_date[0:16] == current_date[0:16] # отрезаем время до минут (т.е 15 символов, но диапазон не отражает символ в последней границе, поэтому +1 в диапазоне


@allure.suite('2_Проверка запроса PUT/UPDATE')
@allure.title('Проверяем запрос PUT/UPDATE c полями: "name" и "job"')
def test_put_update_user_with_name_and_job():  # метод PUT
    body = {
            "name": "morpheus_NEW",
            "job": "leader_NEW"
        }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + UPDATE_USER}'):
        response = httpx.put(BASE_URL + UPDATE_USER, json=body)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()
    with allure.step(f'Валидация схемы'):
        validate(response_json, UPDATE_USER_SCHEME)

    with allure.step(f'Проверяем обновленный "name": {response_json['name']}'):
        assert response_json['name'] == body['name']

    with allure.step(f'Проверяем  обновленный "job": {response_json['job']}'):
        assert response_json['job'] == body['job']

    with allure.step(f'Проверяем "updatedAt"'):
        updatation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updatation_date[0:15] == current_date[0:15]


@allure.suite('2_Проверка запроса PUT/UPDATE')
@allure.title('Проверяем запрос PUT/UPDATE без поля: "job"')
def test_put_update_user_without_job():  # метод PUT
    body = {
            "name": "morpheus_NEW"
        }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + UPDATE_USER}'):
        response = httpx.put(BASE_URL + UPDATE_USER, json=body)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()
    with allure.step(f'Валидация схемы'):
        validate(response_json, UPDATE_USER_SCHEME)

    with allure.step(f'Проверяем обновленный "name": {response_json['name']}'):
        assert response_json['name'] == body['name']

    with allure.step(f'Проверяем "updatedAt"'):
        updatation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updatation_date[0:15] == current_date[0:15]


@allure.suite('2_Проверка запроса PUT/UPDATE')
@allure.title('Проверяем запрос PUT/UPDATE без поля: "name"')
def test_put_update_user_without_name():  # метод PUT
    body = {
            "job": "leader_NEW"
        }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + UPDATE_USER}'):
        response = httpx.put(BASE_URL + UPDATE_USER, json=body)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()
    with allure.step(f'Валидация схемы'):
        validate(response_json, UPDATE_USER_SCHEME)

    with allure.step(f'Проверяем обновленный "job": {response_json['job']}'):
        assert response_json['job'] == body['job']

    with allure.step(f'Проверяем "updatedAt"'):
        updatation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updatation_date[0:15] == current_date[0:15]


@allure.suite('3_Проверка запроса PATCH/UPDATE')
@allure.title('Проверяем запрос PATCH/UPDATE c полями: "name" и "job"')
def test_patch_update_user_with_name_and_job():  # метод PUT
    body = {
            "name": "morpheus_NEW",
            "job": "leader_NEW"
        }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + UPDATE_USER}'):
        response = httpx.put(BASE_URL + UPDATE_USER, json=body)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()
    with allure.step(f'Валидация схемы'):
        validate(response_json, UPDATE_USER_SCHEME)

    with allure.step(f'Проверяем обновленный "name": {response_json['name']}'):
        assert response_json['name'] == body['name']

    with allure.step(f'Проверяем  обновленный "job": {response_json['job']}'):
        assert response_json['job'] == body['job']

    with allure.step(f'Проверяем "updatedAt"'):
        updatation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updatation_date[0:15] == current_date[0:15]


@allure.suite('3_Проверка запроса PATCH/UPDATE')
@allure.title('Проверяем запрос PATCH/UPDATE без поля: "job"')
def test_patch_update_user_without_job():  # метод PUT
    body = {
            "name": "morpheus_NEW"
        }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + UPDATE_USER}'):
        response = httpx.patch(BASE_URL + UPDATE_USER, json=body)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()
    #print(response_json)
    with allure.step(f'Валидация схемы'):
        validate(response_json, UPDATE_USER_SCHEME)

    with allure.step(f'Проверяем обновленный "name": {response_json['name']}'):
        assert response_json['name'] == body['name']

    with allure.step(f'Проверяем "updatedAt"'):
        updatation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updatation_date[0:15] == current_date[0:15]


@allure.suite('3_Проверка запроса PATCH/UPDATE')
@allure.title('Проверяем запрос PATCH/UPDATE без поля!!!: "name"')
def test_patch_update_user_without_name():  # метод PUT
    body = {
            "job": "resident_NEW"
        }
    with allure.step(f'Делаем запрос по адресу: {BASE_URL + UPDATE_USER}'):
        response = httpx.patch(BASE_URL + UPDATE_USER, json=body)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()
    #print(response_json)
    with allure.step(f'Валидация схемы'):
        validate(response_json, UPDATE_USER_SCHEME)

    with allure.step(f'Проверяем обновленный "job": {response_json['job']}'):
        assert response_json['job'] == body['job']

    with allure.step(f'Проверяем "updatedAt"'):
        updatation_date = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updatation_date[0:15] == current_date[0:15]


@allure.suite('4_Проверка запроса DELETE')
@allure.title('Проверяем запрос DELETE')
def test_delete_user():
    with allure.step(f'Делаем запрос по адресу:   {BASE_URL + UPDATE_USER}'):
        response = httpx.delete(BASE_URL + UPDATE_USER)
    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 204

