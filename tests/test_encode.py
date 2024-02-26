import encoding_standard
from encoding_standard import failure_message
import requests
import urls

def create_to_maj_standard():
    standard = encoding_standard.create(
        charset = {
            "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I",
            "j": "J", "k": "K", "l": "L", "m": "M","n": "N", "o": "O", "p": "P", "q": "Q", "r": "R",
            "s": "S","t": "T", "u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z"
        },
        encoded_char_len = 1,
        encoded_char_sep = "",
        case_sensitive = True,
        allowed_unrefenced_chars = True
    )
    requests.post(urls.CREATE_STANDARD, json=standard)

    return standard

def create_morse_standard():
    standard = encoding_standard.create(
        charset = {
            "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..",
            "j": ".---", "k": "-.-", "l": ".-..", "m": "--","n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.",
            "s": "...","t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--.."
        },
        encoded_char_len = None,
        encoded_char_sep = " ",
        case_sensitive = False,
        allowed_unrefenced_chars = False
    )
    requests.post(urls.CREATE_STANDARD, json=standard)

    return standard

def test_encode_morse():
    standard = create_morse_standard()

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_name": standard["name"],
        "string": "abc"
    })

    assert response.status_code == 200, failure_message(response)
    assert response.json()["encoded_string"] == ".- -... -.-.", failure_message(response)


def test_encode():
    standard = create_to_maj_standard()

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_name": standard["name"],
        "string": "abc"
    })

    assert response.status_code == 200, failure_message(response)
    assert response.json()["encoded_string"] == "ABC", failure_message(response)

def test_encode_with_unreferenced_chars():
    standard = create_to_maj_standard()

    response = requests.post(urls.ENCODE, json={
        "encoding_standard_name": standard["name"],
        "string": "abc/def"
    })

    assert response.status_code == 200, failure_message(response)
    assert response.json()["encoded_string"] == "ABC/DEF", failure_message(response)




def test_encode_with_non_existent_standard():
    response = requests.post(urls.ENCODE, json={
        "encoding_standard_name": "non-existent-standard",
        "string": "abc"
    })

    assert response.status_code == 404, failure_message(response)