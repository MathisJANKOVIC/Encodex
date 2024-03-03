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

def remove_id(standard: dict) -> dict:
    """Returns a dictionary representation of the encoding standard without the id."""
    standard.pop("id", None)
    return standard

def wrong_status_code_message(status_code: int, expected_status_code: int) -> str:
    """Returns a message indicating that the status code was not the expected one."""
    return f"expected status code {expected_status_code}, got {status_code}"