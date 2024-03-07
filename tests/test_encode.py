import requests
import random
import standard
import urls

def wrong_encoded_str_message(encoded_string: str, expected_encoded_string: str) -> str:
    return f"expected encoded string to be '{expected_encoded_string}', not '{encoded_string}'"



def test_encode_using_to_maj_standard():
    std_response = standard.create_maj().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "test"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "TEST", wrong_encoded_str_message(encoded_str, "TEST")

def test_encode_using_to_maj_standard_with_unreferenced_char():
    std_response = standard.create_maj().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "test !"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "TEST !", wrong_encoded_str_message(encoded_str, "TEST !")

def test_encode_using_morse_standard():
    std_response = standard.create_morse().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "this is a test"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "- .... .. ... / .. ... / .- / - . ... -", wrong_encoded_str_message(encoded_str, "- .... .. ... / .. ... / .- / - . ... -")

def test_encode_using_morse_standard_with_unreferenced_char():
    std_response = standard.create_morse().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "/Novak Djokovic is the GOAT/"
    })
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_encode_using_morse_standard_sending_uppercase_chars():
    std_response = standard.create_morse().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "SOS"
    })
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "... --- ...", wrong_encoded_str_message(encoded_str, "... --- ...")

def test_encode_using_non_existent_standard():
    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": random.randint(100, 100_000_000),
        "string": "azerty"
    })
    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)
