import standard
import urls
import requests
import random

def wrong_decoded_str_message(encoded_string: str, expected_encoded_string: str) -> str:
    return f"expected decoded string to be '{expected_encoded_string}', not '{encoded_string}'"


def test_decode_using_to_maj_standard():
    std_response = standard.create_maj().json()["encoding_standard"]

    response = requests.post(urls.DECODE, json={
        "encoding_standard_id": std_response["id"],
        "encoded_string": "TEST"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    decoded_str = response.json()["decoded_string"]
    assert decoded_str == "test", wrong_decoded_str_message(decoded_str, "test")

def test_decode_using_to_maj_standard_with_unreferenced_char():
    std_response = standard.create_maj().json()["encoding_standard"]

    response = requests.post(urls.DECODE, json={
        "encoding_standard_id": std_response["id"],
        "encoded_string": "TEST !"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    decoded_str = response.json()["decoded_string"]
    assert decoded_str == "test !", wrong_decoded_str_message(decoded_str, "test !")

def test_decode_using_morse_standard():
    std_response = standard.create_morse().json()["encoding_standard"]

    response = requests.post(urls.DECODE, json={
        "encoding_standard_id": std_response["id"],
        "encoded_string": "- .... .. ... / .. ... / .- / - . ... -"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    decoded_str = response.json()["decoded_string"]
    assert decoded_str == "this is a test", wrong_decoded_str_message(decoded_str, "this is a test")

def test_decode_using_morse_standard_with_unreferenced_char():
    std_response = standard.create_morse().json()["encoding_standard"]

    response = requests.post(urls.DECODE, json={
        "encoding_standard_id": std_response["id"],
        "encoded_string": "/Novak Djokovic is the GOAT/"
    })

    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_decode_using_morse_standard_sending_uppercase_chars():
    std_response = standard.create_morse().json()["encoding_standard"]

    response = requests.post(urls.DECODE, json={
        "encoding_standard_id": std_response["id"],
        "encoded_string": "... --- ..."
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    decoded_str = response.json()["decoded_string"]
    assert decoded_str == "sos", wrong_decoded_str_message(decoded_str, "sos")

def test_decode_using_non_existent_standard():
    response = requests.post(urls.DECODE, json={
        "encoding_standard_id": random.randint(100, 100_000_000),
        "encoded_string": "azerty"
    })

    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)