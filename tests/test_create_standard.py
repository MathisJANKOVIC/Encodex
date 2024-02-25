from encoding_standard import failure_message
import encoding_standard
import requests
import urls

def test_create_standard():
    response = requests.post(urls.CREATE_STANDARD, json=encoding_standard.create())
    assert response.status_code == 201, failure_message(response)

def test_create_duplicate_standard():
    standard = encoding_standard.create()
    requests.post(urls.CREATE_STANDARD, json=standard)

    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 409, failure_message(response)

def test_create_standard_with_too_short_name():
    standard = encoding_standard.create("ax")
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_too_long_name():
    standard = encoding_standard.create("h" * 37)
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_special_char_in_name():
    standard = encoding_standard.create("encoding#standard")
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_non_unique_encoded_chars():
    standard = encoding_standard.create(charset={"a": "A", "b": "A"})
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_null_encoded_char_len_and_empty_encoded_char_sep():
    standard = encoding_standard.create(encoded_char_len=None, encoded_char_sep="")
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_char_len_different_than_1():
    standard = encoding_standard.create(charset={"": "A"})
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_null_encoded_char_len_and_empty_encoded_char():
    standard = encoding_standard.create(charset={"a": ""}, encoded_char_len=None)
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_encoded_char_len_not_matching():
    standard = encoding_standard.create(charset={"a": "rs"}, encoded_char_len=1)
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_encoded_char_sep_in_encoded_char():
    standard = encoding_standard.create(charset={"a": "b/x"}, encoded_char_sep="/")
    response = requests.post(urls.CREATE_STANDARD, json=standard)
    assert response.status_code == 422, failure_message(response)