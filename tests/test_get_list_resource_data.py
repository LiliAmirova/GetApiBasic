import httpx
from jsonschema import validate
from core.contracts import LIST_DATA_SCHEME
import allure

BASE_URL = "https://reqres.in/"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"

COLOR_START = "#"
YEAR_START = "200"
PANTONE = "-"

@allure.suite('Проверка запросов данных ВСЕХ ресурсов')
@allure.title('Проверяем получение СПИСКА ресурсов')
def test_list_resource():
    with allure.step(f'Делаем запрос по адресу: {BASE_URL+LIST_RESOURCE}'):
        response = httpx.get(BASE_URL + LIST_RESOURCE)

    with allure.step(f'Проверяем код ответа'):
        assert response.status_code == 200


    data = response.json()['data']
    for item in data:
        with allure.step(f'Проверяем элемент из списка: {item['id']}'):
            validate(item, LIST_DATA_SCHEME)   # проверка json-схемы

            b = len(str(item['year']))
            if b > 5:  # year состоит из 4 символов и проверка окончания
                print(f'Неверный формат атрибута:{item['year']} ')
                break
            with allure.step('Проверяем связь year и id'):  # Проверка атрибута "year"
                assert str(item['year']).endswith(YEAR_START + str((item['id'] - 1)))

            with allure.step('Проверяем первый символ "#" в color'): # Проверка атрибута 'color'
                assert item['color'].startswith(COLOR_START) # проверка, что код цвета начинается с символа #

            a = len(item['color']) # color состоит из 6 символов
            if a > 7:
                print(f'Hex-код data.сolor: {item['color']} содержит более 6 символов')
                break

            with allure.step('Проверяем наличие "-" в pantone_value'):  # Проверка атрибута 'pantone_value': наличие "-"
                assert PANTONE in item['pantone_value']


@allure.suite('Проверка запросов данных ВСЕХ ресурсов')
@allure.title('Проверяем получение данных ОДНОГО ресурса')
def test_single_resource():
    with allure.step(f'Делаем запрос по адресу:{BASE_URL + SINGLE_RESOURCE}'):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE)

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    data = response.json()['data']
    with allure.step('Проверяем первый символ "#"в color'):
        assert data['color'].startswith(COLOR_START)

    with allure.step('Проверяем наличие "-" в pantone_value'):
        assert PANTONE in data['pantone_value']

@allure.suite('Проверка запросов данных ВСЕХ ресурсов')
@allure.title('Проверяем ОТСУТСТВИЕ данных по ресурсу')
def test_resource_not_found():
    with allure.step(f'Делаем запрос по адресу:{BASE_URL + SINGLE_RESOURCE_NOT_FOUND}'):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404

