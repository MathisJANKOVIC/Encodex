from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.models import EncodingType
from database.connection import LocalSession

router = APIRouter()

@router.get("/encodex/")
def get_all_encoding_types():

    session = LocalSession()
    encoding_types: list[EncodingType] = session.query(EncodingType).all()

    encoding_types = [{
            "id": encoding_type.id,
            "name": encoding_type.name,
            "encoded_char_length": encoding_type.encoded_chars_len,
            "encoded_chars_sep": encoding_type.encoded_chars_sep,
            "encoded_words_sep": encoding_type.encoded_words_sep ,
            "encoding_chars": {encoding_char.char: encoding_char.encoded_char for encoding_char in encoding_type.encoding_chars}
        } for encoding_type in encoding_types
    ]

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": encoding_types})

@router.get("/encodex/{encoding_type_name}")
def get_encoding_type(encoding_type_name: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    encoding_type = {
        "id": encoding_type.id,
        "name": encoding_type.name,
        "encoding_chars": {encoding_char.char: encoding_char.encoded_char for encoding_char in encoding_type.encoding_chars},
        "encoded_char_length": encoding_type.encoded_chars_len,
        "encoded_chars_sep": encoding_type.encoded_chars_sep,
        "encoded_words_sep": encoding_type.encoded_words_sep
    }

    session.close()
    return JSONResponse(status_code=200, content = {"succes": True, "content": encoding_type})