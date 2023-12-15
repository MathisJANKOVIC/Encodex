from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingType
from database.connection import LocalSession

class EncodingTypeModel(BaseModel):
    encoding_chars: dict[str, str]
    is_case_sensitive: bool = False
    encoded_chars_sep: str = ""
    encoded_words_sep: str = ""

router = APIRouter()

@router.post("/encodex/{encoding_type_name}/create/")
def create_encoding_type(encoding_type_name: str, new_encoding_type: EncodingTypeModel = Body(...)):

    session = LocalSession()

    if(session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first() is not None):
        session.close()
        return JSONResponse(status_code=409, content={"Succes": False, "message": "Encoding type already exists"})

    if(not new_encoding_type.is_case_sensitive):
        for char in new_encoding_type.encoding_chars.keys():
            new_encoding_type.encoding_chars[char] = new_encoding_type.encoding_chars[char].lower()

    encoded_chars_lens = set()
    for char, encoded_char in new_encoding_type.encoding_chars.items():
        if(len(char) != 1):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoding characters keys must be one character long"})
        if(len(encoded_char) == 0):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot be empty"})
        if(new_encoding_type.encoded_chars_sep != "" and new_encoding_type.encoded_chars_sep in encoded_char or new_encoding_type.encoded_words_sep != "" and new_encoding_type.encoded_words_sep in encoded_char):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain separators"})

        encoded_chars_lens.add(len(encoded_char))

    if(len(new_encoding_type.encoding_chars.values()) != len(set(new_encoding_type.encoding_chars.values()))):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters must be unique"})

    if(new_encoding_type.encoded_chars_sep == new_encoding_type.encoded_words_sep and new_encoding_type.encoded_chars_sep != ""):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters and encoded words separators cannot be the same"})

    if(len(encoded_chars_lens) > 1):
        if(new_encoding_type.encoded_chars_sep and new_encoding_type.encoded_words_sep):
            encoded_char_len = None
        else:
            session.close()
            return JSONResponse(
                status_code = 422,
                content = {
                    "succes": False,
                    "message": "Encoded characters have different lengths, "
                        + "please specify encoded characters and encoding words separators"
                        + "or make all encoded characters have the same length"
                })
    else:
        encoded_char_len = encoded_chars_lens

    session.add(EncodingType(
        name = encoding_type_name,
        encoding_chars = new_encoding_type.encoding_chars,
        is_case_sensitive = new_encoding_type.is_case_sensitive,
        encoded_chars_sep = new_encoding_type.encoded_chars_sep,
        encoded_words_sep = new_encoding_type.encoded_words_sep,
        encoded_chars_len = encoded_char_len
    ))

    session.commit()
    session.close()

    return JSONResponse(status_code=201, content={"succes": True, "message": "Encoding type created successfully"})