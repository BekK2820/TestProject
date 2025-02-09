import requests
import pytest
import allure

BASE_URL = 'https://api.restful-api.dev/objects'
SAMPLE_PAYLOAD = {
    "name": "Apple MacBook Pro 16",
    "data": {
        "year": 2019,
        "price": 1849.99,
        "CPU model": "Intel Core i9",
        "Hard disk size": "1 TB"
    }
}

# Фикстура для создания и удаления объекта
@pytest.fixture
def obj_id():
    response = requests.post(BASE_URL, json=SAMPLE_PAYLOAD)
    response.raise_for_status()
    object_id = response.json()['id']
    yield object_id
    delete_response = requests.delete(f'{BASE_URL}/{object_id}')
    delete_response.raise_for_status()

# Тест создания объекта
@allure.feature('Создание объекта')
@allure.story('Проверка создания нового объекта')
@allure.description('Тест проверяет, что объект создается с корректными данными')
def test_create_obj():
    """Тест проверяет, что объект создается с корректными данными."""
    response = requests.post(BASE_URL, json=SAMPLE_PAYLOAD)
    response.raise_for_status()  # Проверка на ошибки HTTP
    created_object = response.json()

    # Проверка статус-кода и данных
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    assert created_object['name'] == SAMPLE_PAYLOAD['name'], "Имя объекта не совпадает"
    assert created_object['data'] == SAMPLE_PAYLOAD['data'], "Данные объекта не совпадают"

# Тест обновления объекта
@allure.feature('Обновление объекта')
@allure.story('Проверка обновления данных объекта')
@allure.description('Тест проверяет, что объект успешно обновляется')
def test_update_objects(obj_id):
    """Тест проверяет, что объект успешно обновляется."""
    updated_payload = {
        "name": "Apple MacBook Pro 20",
        "data": {
            "year": 2020,
            "price": 2049.99,
            "CPU model": "Intel Core i10",
            "Hard disk size": "2 TB"
        }
    }
    response = requests.put(f'{BASE_URL}/{obj_id}', json=updated_payload)
    response.raise_for_status()  # Проверка на ошибки HTTP
    updated_object = response.json()

    # Проверка статус-кода и данных
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    assert updated_object['name'] == updated_payload['name'], "Имя объекта не обновлено"
    assert updated_object['data'] == updated_payload['data'], "Данные объекта не обновлены"




# Параметризованный тест для создания объектов с разными данными
@allure.feature('Параметризованное создание объекта')
@allure.story('Проверка создания объектов с разными данными')
@allure.description('Тест проверяет создание объектов с разными параметрами')
@pytest.mark.parametrize("name, year", [
    ("Apple MacBook Pro 16", 2019),
    ("Apple MacBook Pro 20", 2020),
    ("Dell XPS 15", 2021)
])
def test_create_obj_with_params(name, year):
    """Параметризованный тест для создания объектов с разными данными."""
    payload = {
        "name": name,
        "data": {
            "year": year,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    response = requests.post(BASE_URL, json=payload)
    response.raise_for_status()  # Проверка на ошибки HTTP
    created_object = response.json()

    # Проверка статус-кода и данных
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"
    assert created_object['name'] == name, "Имя объекта не совпадает"
    assert created_object['data']['year'] == year, "Год объекта не совпадает"

    # Удаление созданного объекта
    object_id = created_object['id']
    delete_response = requests.delete(f'{BASE_URL}/{object_id}')
    delete_response.raise_for_status()
