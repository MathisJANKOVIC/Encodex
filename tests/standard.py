import requests
import random
import uuid
import urls

class Standard:
    id: int
    name: str
    case_sensitive: bool
    allowed_unrefenced_chars: bool
    encoded_char_len: int | None
    encoded_char_sep: str
    charset: dict[str, str]

    def __init__(self,
        name: str = None,
        case_sensitive: bool = False,
        allowed_unrefenced_chars: bool = False,
        encoded_char_len: int | None = None,
        encoded_char_sep: str = " ",
        charset: dict[str, str] = {"a": "A", "b": "B", "c": "C"}
    ):
        self.id = random.randint(100, 100_000_000)

        if(name is None):
            self.name = str(uuid.uuid4())
        else:
            self.name = name

        self.case_sensitive = case_sensitive
        self.allowed_unrefenced_chars = allowed_unrefenced_chars
        self.encoded_char_len = encoded_char_len
        self.encoded_char_sep = encoded_char_sep
        self.charset = charset

    def create(self, expected_status_code: int = 201):
        response = requests.post(urls.CREATE_STANDARD, json=self.__dict__)
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

        if(response.status_code == 201):
            standard_response = response.json()["encoding_standard"]
            self.id = standard_response["id"]
            assert self.__dict__ == standard_response, "response encoding standard does not match the sent one"

    def update_charset(self, codepoints: dict, expected_status_code: int = 200):
        self.charset = {**self.charset, **codepoints}

        response = requests.patch(urls.UPDATE_STANDARD, json={
            "encoding_standard_id": self.id,
            "charset": self.charset
        })
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

        if(response.status_code == 200):
            assert self.__dict__ == response.json()["encoding_standard"], "response encoding standard does not match the sent one"

    def rename(self, new_name: str = None, expected_status_code: int = 200):
        if(new_name is None):
            new_name = str(uuid.uuid4())

        self.name = new_name

        response = requests.put(urls.RENAME_STANDARD, json={
            "encoding_standard_id": self.id,
            "new_name": new_name
        })
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

        if(response.status_code == 200):
            assert self.__dict__ == response.json()["encoding_standard"], response.json()["encoding_standard"]

    def delete(self, expected_status_code: int = 200):
        response = requests.delete(f"{urls.DELETE_STANDARD}/{self.id}")
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

    def get(self, expected_status_code: int = 200):
        response = requests.get(f"{urls.GET_STANDARDS}/{self.id}")
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

        if(response.status_code == 200):
            assert self.__dict__ == response.json()["encoding_standard"], "response encoding standard does not match the created one"

    @staticmethod
    def get_all(expected_status_code: int = 200) -> list[dict]:
        response = requests.get(urls.GET_STANDARDS)
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)
        return response.json()["encoding_standards"]

    def decode(self, encoded_string: str, expected_status_code: int = 200) -> str:
        response = requests.post(urls.DECODE, json={
            "encoding_standard_id": self.id,
            "encoded_string": encoded_string
        })
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

        if(response.status_code == 200):
            return response.json()["decoded_string"]

    def encode(self, string: str, expected_status_code: int = 200) -> str:
        response = requests.post(urls.ENCODE, json={
            "encoding_standard_id": self.id,
            "string": string
        })
        assert response.status_code == expected_status_code, Standard.wrong_status_code_message(response.status_code, expected_status_code)

        if(response.status_code == 200):
            return response.json()["encoded_string"]

    @staticmethod
    def wrong_status_code_message(status_code: int, expected_status_code: int) -> str:
        return f"expected status code {expected_status_code}, got {status_code}"

    @staticmethod
    def wrong_decoded_str_message(encoded_string: str, expected_encoded_string: str) -> str:
        return f"expected decoded string to be '{expected_encoded_string}', not '{encoded_string}'"

    @staticmethod
    def wrong_encoded_str_message(encoded_string: str, expected_encoded_string: str) -> str:
        return f"expected encoded string to be '{expected_encoded_string}', not '{encoded_string}'"

    @classmethod
    def new_maj(cls):
        return cls(
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
        )

    @classmethod
    def new_morse(cls):
        return cls(
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
        )
