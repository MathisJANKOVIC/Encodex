import requests
import standard
import urls

def test_create_standard_with_defined_encoded_char_len_and_empty_sep():
    std = standard.create(
        case_sensitive = True,
        allowed_unrefenced_chars = True,
        encoded_char_len = 1,
        encoded_char_sep = "",
        charset = {"a": "A", "b": "B", "c": "C"}
    )
    response = requests.post(urls.CREATE_STANDARD, json=std)

    assert response.status_code == 201, standard.message(response)
    std_response = response.json()["encoding_standard"]
    assert standard.remove_id(std_response) == std, "The response standard does not match the request standard"

def test_create_standard_with_encoded_char_sep_and_undefined_len():
    std = standard.create(
        case_sensitive = False,
        allowed_unrefenced_chars = False,
        encoded_char_len = None,
        encoded_char_sep = "-",
        charset = {"a": "z", "b": "yy", "c": "xxx"}
    )
    response = requests.post(urls.CREATE_STANDARD, json=std)

    assert response.status_code == 201, standard.message(response)
    std_response = response.json()["encoding_standard"]
    assert standard.remove_id(std_response) == std, standard.message(response)

def test_create_duplicate_standard():
    std = standard.create()
    requests.post(urls.CREATE_STANDARD, json=std)

    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 409, standard.message(response)

def test_create_standard_with_too_short_name():
    std = standard.create("ax")
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_too_long_name():
    std = standard.create("s" * 37)
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_special_char_in_name():
    std = standard.create("encoding#standard")
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_encoded_char_len_small_than_1():
    std = standard.create(encoded_char_len=0)
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_undefined_encoded_char_len_and_empty_sep():
    std = standard.create(encoded_char_len=None, encoded_char_sep="")
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_undefined_encoded_char_len_and_empty_encoded_char():
    std = standard.create(charset={"a": ""}, encoded_char_len=1)
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_encoded_char_len_not_matching():
    std = standard.create(charset={"a": "rs"}, encoded_char_len=1)
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_char_len_different_than_1():
    std = standard.create(charset={"aa": "A"})
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_non_unique_encoded_chars():
    std = standard.create(charset={"a": "A", "b": "A", "c": "C"})
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)

def test_create_standard_with_encoded_char_sep_in_encoded_char():
    std = standard.create(charset={"a": "b/x"}, encoded_char_sep="/")
    response = requests.post(urls.CREATE_STANDARD, json=std)
    assert response.status_code == 422, standard.message(response)