import requests
import random
import standard
import urls

def wrong_encoded_str_message(encoded_string: str, expected_encoded_string: str) -> str:
    return f"expected encoded string to be '{expected_encoded_string}', got '{encoded_string}'"

def create_to_maj_standard():
    return requests.post(urls.CREATE_STANDARD, json=standard.create(
        case_sensitive = True,
        allowed_unrefenced_chars = True,
        encoded_char_len = 1,
        encoded_char_sep = "",
        charset = {
            "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G",
            "h": "H","i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N",
            "o": "O", "p": "P","q": "Q", "r": "R", "s": "S", "t": "T", "u": "U",
            "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z"
        }
    ))

def create_morse_standard():
    return requests.post(urls.CREATE_STANDARD, json=standard.create(
        case_sensitive = False,
        allowed_unrefenced_chars = False,
        encoded_char_sep = " ",
        encoded_char_len = None,
        charset = {
            "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.",
            "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.",
            "o": "---", "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-",
            "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..", " ": "/"
        }
    ))

def test_encode_using_to_maj_standard():
    std_response = create_to_maj_standard().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "test"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "TEST", wrong_encoded_str_message(encoded_str, "TEST")

def test_encode_using_to_maj_standard_with_unreferenced_char():
    std_response = create_to_maj_standard().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "test !"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "TEST !", wrong_encoded_str_message(encoded_str, "TEST !")

def test_encode_using_morse_standard():
    std_response = create_morse_standard().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "this is a test"
    })

    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "- .... .. ... / .. ... / .- / - . ... -", wrong_encoded_str_message(encoded_str, "- .... .. ... / .. ... / .- / - . ... -")

def test_encode_using_morse_standard_with_unreferenced_char():
    std_response = create_morse_standard().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "/Novak Djokovic is the GOAT/"
    })
    assert response.status_code == 422, standard.wrong_status_code_message(response.status_code, 422)

def test_encode_using_morse_standard_sending_uppercase_chars():
    std_response = create_morse_standard().json()["encoding_standard"]

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": std_response["id"],
        "string": "SOS"
    })
    assert response.status_code == 200, standard.wrong_status_code_message(response.status_code, 200)
    encoded_str = response.json()["encoded_string"]
    assert encoded_str == "... --- ...", wrong_encoded_str_message(encoded_str, "... --- ...")

def test_encode_using_non_existent_standard():
    response = requests.post(urls.ENCODE, json={
        "encoding_standard_id": random.randint(0, 100_000_000),
        "string": "azerty"
    })
    assert response.status_code == 404, standard.wrong_status_code_message(response.status_code, 404)
