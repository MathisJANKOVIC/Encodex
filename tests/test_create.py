from encoding_standard import failure_message
import encoding_standard
import env
import requests

ENDPOINT_URL = f"{env.BASE_URL}/encodex/create/"

def test_create_encoding_standard():
    response = requests.post(ENDPOINT_URL, json=encoding_standard.create())
    assert response.status_code == 201, failure_message(response)

def test_create_duplicate_encoding_standard():
    standard = encoding_standard.create()
    requests.post(ENDPOINT_URL, json=standard)

    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 409, failure_message(response)

def test_create_encoding_standard_with_too_short_name():
    standard = encoding_standard.create("ax")
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_too_long_name():
    standard = encoding_standard.create("h" * 37)
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_special_char_in_name():
    standard = encoding_standard.create("encoding#standard")
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_non_unique_encoded_chars():
    standard = encoding_standard.create(charset={"a": "A", "b": "A"})
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_null_encoded_char_len_and_empty_encoded_char_sep():
    standard = encoding_standard.create(encoded_char_len=None, encoded_char_sep="")
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_empty_char():
    standard = encoding_standard.create(charset={"": "A"})
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_null_encoded_char_len_and_empty_encoded_char():
    standard = encoding_standard.create(charset={"a": ""}, encoded_char_len=None)
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_encoded_char_len_not_matching():
    standard = encoding_standard.create(charset={"a": "rs"}, encoded_char_len=1)
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_encoding_standard_with_encoded_char_sep_in_encoded_char():
    standard = encoding_standard.create(charset={"a": "b/x"}, encoded_char_sep="/")
    response = requests.post(ENDPOINT_URL, json=standard)
    assert response.status_code == 422, failure_message(response)