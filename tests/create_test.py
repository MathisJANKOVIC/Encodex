from utils import BASE_URL, failure_message
from requests.models import Response
import requests
import uuid

def encoding_standard(name: str, charset: dict = {"a": "A", "b": "B", "c": "C"}, encoded_char_len: int = 1, encoded_char_sep: str = ""):
    return {
        "name": name,
        "case_sensitive": False,
        "charset": charset,
        "allowed_unrefenced_chars": True,
        "encoded_char_len": encoded_char_len,
        "encoded_char_sep": encoded_char_sep
    }

def test_create_standard():
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=encoding_standard(str(uuid.uuid4())))
    assert response.ok, failure_message(response)

def test_create_duplicate_standard():
    standard = encoding_standard(str(uuid.uuid4()))
    requests.post(f"{BASE_URL}/encodex/create/", json=standard)

    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 409, failure_message(response)

def test_create_standard_with_too_short_name():
    standard = encoding_standard("sr")
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_too_long_name():
    standard = encoding_standard("a" * 37)
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_special_chars_in_name():
    standard = encoding_standard("encoding#standard")
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_non_unique_encoded_chars():
    standard = encoding_standard(name=str(uuid.uuid4()), charset={"a": "A", "b": "A"})
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_empty_encoded_char_len_and_sep():
    standard = encoding_standard(name=str(uuid.uuid4()), encoded_char_len=None, encoded_char_sep="")
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_empty_char():
    standard = encoding_standard(name=str(uuid.uuid4()), charset={"": "A"})
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_undefined_encoded_char_len_and_null_encoded_char():
    standard = encoding_standard(name=str(uuid.uuid4()), charset={"a": ""}, encoded_char_len=None)
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_encoded_char_len_not_matching():
    standard = encoding_standard(name=str(uuid.uuid4()), charset={"a": "RS"}, encoded_char_len=1)
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)

def test_create_standard_with_encoded_char_sep_in_encoded_char_and_empty_sep():
    standard = encoding_standard(name=str(uuid.uuid4()), charset={"a": "R#S"}, encoded_char_sep="#")
    response: Response = requests.post(f"{BASE_URL}/encodex/create/", json=standard)
    assert response.status_code == 422, failure_message(response)