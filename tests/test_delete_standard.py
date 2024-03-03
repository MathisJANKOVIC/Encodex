import requests
import random
import standard
import urls

def test_delete_standard():
    response = requests.post(urls.CREATE_STANDARD, json=standard.create())
    std_response = response.json()["encoding_standard"]

    response = requests.delete(f"{urls.DELETE_STANDARD}/{std_response["id"]}")
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)

def test_delete_not_existing_standard():
    response = requests.delete(f"{urls.DELETE_STANDARD}/{random.randint(0, 100_000_000)}")
    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)