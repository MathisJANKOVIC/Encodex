import uuid
import requests
import urls
def create(
    name: str = None,
    case_sensitive: bool = False,
    allowed_unrefenced_chars: bool = False,
    encoded_char_len: int | None = None,
    encoded_char_sep: str = " ",
    charset: dict[str, str] = {"a": "A", "b": "B", "c": "C"},
) -> dict:

    if(name is None):
        name = str(uuid.uuid4())

    return {
        "name": name,
        "case_sensitive": case_sensitive,
        "allowed_unrefenced_chars": allowed_unrefenced_chars,
        "encoded_char_len": encoded_char_len,
        "encoded_char_sep": encoded_char_sep,
        "charset": charset
    }

def remove_id(standard: dict) -> dict:
    """Returns a dictionary representation of the encoding standard without the id."""
    standard.pop("id", None)
    return standard

def wrong_status_code_message(status_code: int, expected_status_code: int) -> str:
    """Returns a message indicating that the status code was not the expected one."""
    return f"expected status code {expected_status_code}, got {status_code}"

def create_maj():
    return requests.post(urls.CREATE_STANDARD, json=create(
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

def create_morse():
    return requests.post(urls.CREATE_STANDARD, json=create(
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