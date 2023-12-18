from typing import Optional

from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingStandard
from database.connection import LocalSession

class EncodingStandardModel(BaseModel):
    name: str
    case_sensitive: bool
    allowed_unrefenced_chars: Optional[bool] = False
    encoded_char_len: Optional[int] = None
    encoded_char_sep: str
    encoded_word_sep: str
    charset: dict[str, str]

router = APIRouter()

@router.post("/encodex/create/")
def create_encoding_standard(encoding_standard: EncodingStandardModel = Body(...)):

    session = LocalSession()

    if(session.query(EncodingStandard).filter(EncodingStandard.name == encoding_standard.name).first() is not None):
        session.close()
        return JSONResponse(status_code=409, content={
            "succes": False,
            "message": f"Character encoding standard `{encoding_standard.name}` already exists"
        })

    if(len(encoding_standard.name) < 3):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Character encoding standard name must have at least 3 characters"})

    if(len(encoding_standard.name) > 64):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Character encoding standard name must have at most 64 characters"})

    if(not encoding_standard.name.replace(" ","").replace("-","").replace("_","").isalnum()):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Character encoding standard name cannot contain special characters"})

    if(len(encoding_standard.charset.values()) != len(set(encoding_standard.charset.values()))):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters must be unique"})

    if(encoding_standard.encoded_char_sep == encoding_standard.encoded_word_sep and encoding_standard.encoded_char_sep != ""):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters and encoded words separators cannot be equal"})

    if(encoding_standard.encoded_char_len is None and (encoding_standard.encoded_char_len == "" or encoding_standard.encoded_word_sep == "")):
        session.close()
        return JSONResponse(status_code=422, content={
            "succes": False,
            "message": "if encoded character length is not defined, encoded character and encoded word separators must be defined"
        })

    if(not encoding_standard.case_sensitive):
        encoding_standard.charset = {char.lower(): encoded_char for char, encoded_char in encoding_standard.charset.items()}

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
            return JSONResponse(status_code=422, content={
                "succes": False,
                "message": "Encoded characters lenght must be the same as defined in character encoding standard"
            })

        if(encoding_standard.encoded_char_sep in encoded_char and len(encoding_standard.encoded_char_sep) > 0 or
            encoding_standard.encoded_word_sep in encoded_char and len(encoding_standard.encoded_word_sep) > 0):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain separators"})

    session.add(EncodingStandard(
        name = encoding_standard.name,
        case_sensitive = encoding_standard.case_sensitive,
        allowed_unrefenced_chars = encoding_standard.allowed_unrefenced_chars,
        encoded_char_len = encoding_standard.encoded_char_len,
        encoded_char_sep = encoding_standard.encoded_char_sep,
        encoded_word_sep = encoding_standard.encoded_word_sep,
        charset = encoding_standard.charset
    ))

    session.commit()
    session.close()

    return JSONResponse(status_code=201, content={"succes": True, "message": "Character encoding standard created successfully"})