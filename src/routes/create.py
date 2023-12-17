from typing import Optional

from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingStandard
from database.connection import LocalSession

class EncodingStandardModel(BaseModel):
    name: str
    charset: dict[str, str]
    case_sensitive: Optional[bool] = True
    allowed_unrefenced_chars: Optional[bool] = False

    encoded_char_len: Optional[int] = None
    encoded_char_sep: Optional[str] = ""
    encoded_word_sep: Optional[str] = " "

router = APIRouter()

@router.post("/encodex/create/")
def create_encoding_standard(encoding_standard: EncodingStandardModel = Body(...)):

    session = LocalSession()

    if(session.query(EncodingStandard).filter(EncodingStandard.name == encoding_standard.name).first() is not None):
        session.close()
        return JSONResponse(status_code=409, content={"Succes": False, "message": f"Character encoding standard named '{encoding_standard.name}' already exists"})

    if(not encoding_standard.case_sensitive):
        for char in encoding_standard.charset.keys():
            encoding_standard.charset[char] = encoding_standard.charset[char].lower()


    if(len(encoding_standard.charset.values()) != len(set(encoding_standard.charset.values()))):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters must be unique"})

    if(encoding_standard.encoded_char_sep == encoding_standard.encoded_word_sep and encoding_standard.encoded_char_sep != ""):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters and encoded words separators cannot be equal"})

    for char, encoded_char in encoding_standard.charset.items():
        if(len(char) != 1):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Characters must be one character long"})

        if(encoding_standard.encoded_char_len is None):
            if(len(encoded_char) == 0):
                session.close()
                return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot be empty"})
        elif(len(encoded_char) != encoding_standard.encoded_char_len):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters must have the same length as specified in the encoding standard"})

        if(encoding_standard.encoded_char_sep != "" and encoding_standard.encoded_char_sep in encoded_char or encoding_standard.encoded_word_sep != "" and encoding_standard.encoded_word_sep in encoded_char):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain separators"})

    session.add(EncodingStandard(
        name = encoding_standard.name,
        charset = encoding_standard.charset,
        case_sensitive = encoding_standard.case_sensitive,
        allowed_unrefenced_chars = encoding_standard.allowed_unrefenced_chars,
        encoded_char_len = encoding_standard.encoded_char_len,
        encoded_char_sep = encoding_standard.encoded_char_sep,
        encoded_word_sep = encoding_standard.encoded_word_sep
    ))

    session.commit()
    session.close()

    return JSONResponse(status_code=201, content={"succes": True, "message": "Character encoding standard created successfully"})