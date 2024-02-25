from encoding_standard import failure_message
import encoding_standard
import requests
import urls

def test_add_new_encoding_chars_to_standard():
    standard = encoding_standard.create()
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"a": "z", "b": "x", "c": "y"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 200, response

def test_update_standard_encoding_chars():
    standard = encoding_standard.create(charset={"a": "A", "b": "B", "c": "C"})
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"d": "D", "e": "e", "f": "F"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 200, failure_message(response)

def test_update_not_existing_standard():
    updated_standard = {
        "encoding_standard_name": "not-existing-encoding-standard",
        "charset": {"!": "x"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 404, failure_message(response)

def test_add_non_unique_encoding_char_to_standard():
    standard = encoding_standard.create(charset={"a": "A", "b": "B", "c": "C"})
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"d": "A"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 422, failure_message(response)

def test_add_char_with_len_different_than_1_to_standard():
    standard = encoding_standard.create()
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"ab": "x"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 422, failure_message(response)

def test_add_empty_encoded_char_to_standard():
    standard = encoding_standard.create()
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"a": ""}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 422, failure_message(response)

def test_add_encoded_char_len_not_matching_to_standard():
    standard = encoding_standard.create(encoded_char_len=1)
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"a": "rs"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 422, failure_message(response)

def test_add_encoding_char_with_encoded_char_sep_in_encoded_char_to_standard():
    standard = encoding_standard.create(encoded_char_sep="/")
    requests.post(urls.CREATE_STANDARD, json=standard)

    updated_standard = {
        "encoding_standard_name": standard["name"],
        "charset": {"a": "b/x"}
    }

    response = requests.patch(urls.UPDATE_STANDARD, json=updated_standard)
    assert response.status_code == 422, failure_message(response)
