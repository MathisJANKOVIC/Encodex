from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingType, EncodingChar

class BodyModel(BaseModel):
    encoding_chars: dict

def encoding_char_to_dict(encoding_char):
    return {key: value for key, value in encoding_char.__dict__.items() if not key.startswith('_sa_')}

def encoding_chars_to_dicts(encoding_chars):
    return [encoding_char_to_dict(encoding_char) for encoding_char in encoding_chars]

router = APIRouter()

@router.patch("/encodex/{encoding_type_name}/update/")
def update_encoding_char(encoding_type_name: str, body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_type: EncodingType = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    for char, encoded_char in body.encoding_chars.items():
        if(len(char) != 1):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoding characters keys must be one character long"})
        elif(len(encoded_char) == 0):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot be empty"})
        elif(encoding_type.encoded_chars_sep != "" and encoding_type.encoded_chars_sep in encoded_char or encoding_type.encoded_words_sep != "" and encoding_type.encoded_words_sep in encoded_char):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain separators"})

        existing_encoding_char = session.query(EncodingChar).filter(EncodingChar.char == char).first()

        if(existing_encoding_char is not None):
            encoding_type.encoding_chars.append(EncodingChar(char, encoded_char))
        else:
            existing_encoding_char.encoded_char = encoded_char

    session.add(encoding_type)
    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding type updated successfully"})