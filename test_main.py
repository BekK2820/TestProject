import requests
import pytest
import allure

@pytest.fixture()
def obj_id():
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    response = requests.post('https://api.restful-api.dev/objects', json=payload).json()
    yield response['id']
    requests.delete(f'https://api.restful-api.dev/objects/{response["id"]}')

def test_create_obj():
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    response = requests.post('https://api.restful-api.dev/objects', json=payload).json()
    assert response['name'] == payload['name']


@allure.feature('имя теста, например тест кнопки')
@allure.story('какой раздел функционала тестится')
def test_update_objects():
    payload = {
        "name": "Apple MacBook Pro 20",
        "data": {
            "year": 2020,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    response = requests.put(
        'https://api.restful-api.dev/objects/ff808181932badb60194ae03c8f00b28',
        json=payload
    ).json()
    assert response['name'] ==payload['name']

def test_delete_objects(obj_id):
    response = requests.delete('https://api.restful-api.dev/objects/{}'.format(obj_id))
    assert response.status_code==200
    response = requests.get('https://api.restful-api.dev/objects/{}'.format(obj_id))
    assert response.status_code==404


