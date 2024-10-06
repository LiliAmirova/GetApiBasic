import httpx
from jsonschema import validate
from core.contracts import LIST_DATA_SCHEME

BASE_URL = "https://reqres.in/"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"

COLOR_START = "#"
YEAR_START = "200"
PANTONE = "-"

def test_list_resource():
    response = httpx.get(BASE_URL + LIST_RESOURCE)
    assert response.status_code == 200

    data = response.json()['data']
    for item in data:
        validate(item, LIST_DATA_SCHEME)
        # Проверка атрибута "year"
        # year состоит из 4 символов и проверка окончания
        b = len(str(item['year']))
        if b > 5:
            print(f'Неверный формат атрибута:{item['year']} ')
            break
        assert str(item['year']).endswith(YEAR_START + str((item['id'] - 1)))

        # Проверка атрибута 'color'
        assert item['color'].startswith(COLOR_START) # проверка, что код цвета начинается с символа #
        # color состоит из 6 символов
        a = len(item['color'])
        if a > 7:
            print(f'Hex-код data.сolor: {item['color']} содержит более 6 символов')
            break
        # Проверка атрибута 'pantone_value': наличие "-"
        assert PANTONE in item['pantone_value']

def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200
    data = response.json()['data']
    assert data['color'].startswith(COLOR_START)
    assert PANTONE in data['pantone_value']

def test_resource_not_found():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND)
    assert response.status_code == 404

