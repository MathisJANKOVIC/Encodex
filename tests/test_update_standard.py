import requests
import random
import standard
import urls

def test_add_new_chars_to_standard():
    std = standard.create(case_sensitive=True, charset={"a": "A", "b": "B", "c": "C"})
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"d": "D", "e": "E", "f": "F"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)

    assert (
        {**std["charset"], **update_std_body["charset"]} == response.json()["encoding_standard"]["charset"]
    ), "response encoding standard charset is not as expected after update"


def test_update_standard_by_overriding_some_chars():
    std = standard.create(charset={"a": "A", "b": "B", "c": "x"})
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"c": "c", "d": "D", "e": "e"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)

    assert (
        {**std["charset"], **update_std_body["charset"]} == response.json()["encoding_standard"]["charset"]
    ), "response encoding standard charset is not as expected after update"

def test_update_not_existing_standard():
    update_std_body = {
        "encoding_standard_id": random.randint(100, 100_000_000),
        "charset": {"!": "x"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)

def test_add_non_unique_encoded_char_to_standard():
    std = standard.create(charset={"a": "A", "b": "B", "c": "C"})
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"d": "C"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_add_char_with_len_different_than_1_to_standard():
    std = standard.create()
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"ab": "x"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_add_empty_encoded_char_to_standard():
    std = standard.create()
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"x": ""}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_add_encoded_char_len_not_matching_to_standard():
    std = standard.create(encoded_char_len=1)
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"a": "rs"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_update_standard_with_encoded_char_containing_encoded_char_sep():
    std = standard.create(encoded_char_sep="/")
    std_response = requests.post(urls.CREATE_STANDARD, json=std).json()["encoding_standard"]

    update_std_body = {
        "encoding_standard_id": std_response["id"],
        "charset": {"a": "b/x"}
    }
    response = requests.patch(urls.UPDATE_STANDARD, json=update_std_body)
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)
