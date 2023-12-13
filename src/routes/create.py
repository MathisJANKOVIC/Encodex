from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingType
from database.connection import LocalSession

class BodyModel(BaseModel):
    encoding_chars: dict[str, str]
    encoded_chars_sep: str = ""
    encoded_words_sep: str = ""

router = APIRouter()

@router.post("/encodex/{encoding_type_name}/create/")
def create_encoding_type(encoding_type_name: str, body: BodyModel = Body(...)):

    session = LocalSession()

    if(session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first() is not None):
        session.close()
        return JSONResponse(status_code=409, content={"Succes": False, "message": "Encoding type already exists"})

    encoded_chars_lens = set()
    for char, encoded_char in body.encoding_chars.items():
        if(len(char) != 1):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoding characters keys must be one character long"})
        elif(len(encoded_char) == 0):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot be empty"})
        elif(body.encoded_chars_sep != "" and body.encoded_chars_sep in encoded_char or body.encoded_words_sep != "" and body.encoded_words_sep in encoded_char):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain separators"})

        encoded_chars_lens.add(len(encoded_char))

    if(len(body.encoding_chars.values()) != len(set(body.encoding_chars.values()))):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters must be unique"})
    if(body.encoded_chars_sep == body.encoded_words_sep and body.encoded_chars_sep != ""):
        session.close()
        return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters and encoded words separators cannot be the same"})

    if(len(encoded_chars_lens) > 1):
        if(not body.encoded_chars_sep or not body.encoded_words_sep):
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
            session.add(EncodingType(encoding_type_name, body.encoding_chars, body.encoded_chars_sep, body.encoded_words_sep, None))
    else:
        session.add(EncodingType(encoding_type_name, body.encoding_chars, body.encoded_chars_sep, body.encoded_words_sep, encoded_chars_lens))

    session.commit()
    session.close()

    return JSONResponse(status_code=201, content={"succes": True, "message": "Encoding type created successfully"})