from requests.models import Response
import uuid

def create(
    name: str = None,
    case_sensitive: bool = False,
    allowed_unrefenced_chars: bool = False,
    encoded_char_len: int | None = None,
    encoded_char_sep: str = " ",
    charset: dict[str, str] = {"a": "A", "b": "B", "c": "C"},
) -> dict[str, str]:
    """Creates a dictionary represation of an encoding standard with default values for unspecified fields."""

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

def failure_message(response: Response) -> str:
    """Returns the error message from the response or the response text if the error message is not present."""
    return response.json().get("detail") or response.text