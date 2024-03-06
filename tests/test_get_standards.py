import requests
import random
import standard
import urls

def test_get_all_standards():
    response = requests.get(urls.GET_STANDARDS)
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)

def test_get_all_standards_and_if_created_standard_is_in_it():
    std1 = standard.create()
    requests.post(urls.CREATE_STANDARD, json=std1)

    std2 = standard.create()
    requests.post(urls.CREATE_STANDARD, json=std2)

    response = requests.get(urls.GET_STANDARDS)
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)

    standards = [standard for standard in response.json()["content"] if standard["name"] == std1["name"] or standard["name"] == std2["name"]]
    assert len(standards) == 2, "expected to find 2 standards with the names of the created ones, found: " + str(len(standards))

    assert standard.remove_id(standards[0]) == std1, "created standard not found in the list of all standards"
    assert standard.remove_id(standards[1]) == std2, "created standard not found in the list of all standards"

def test_get_standard():
    std = standard.create()
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]
    response = requests.get(f"{urls.GET_STANDARDS}/{std_response['id']}")

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    assert standard.remove_id(response.json()["content"]) == std, "encoding standard does not match the created one"

def test_get_non_existent_standard():
    response = requests.get(f"{urls.GET_STANDARDS}/{random.randint(100, 100_000_000)}")
    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)
