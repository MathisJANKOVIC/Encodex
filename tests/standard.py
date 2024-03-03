from requests.models import Response
import uuid

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

def message(response: Response) -> str:
    """Return an appropriate message from a requests response to the API."""
    return response.json().get("detail") or response.text

def remove_id(standard: dict) -> dict:
    """Returns a dictionary representation of the encoding standard without the id from a requests response to the API."""
    standard.pop("id", None)
    return standard
