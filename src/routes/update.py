from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingStandard, CodePoint

class BodyModel(BaseModel):
    encoding_chars: dict

router = APIRouter()

@router.patch("/encodex/{encoding_type_name}/update/")
def update_encoding_char(encoding_type_name: str, body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_type: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    for char, encoded_char in body.encoding_chars.items():
        if(len(char) != 1):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoding characters keys must be one character long"})
        if(len(encoded_char) == 0):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot be empty"})
        if(encoding_type.encoded_char_sep != "" and encoding_type.encoded_char_sep in encoded_char or encoding_type.encoded_word_sep != "" and encoding_type.encoded_words_sep in encoded_char):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain separators"})

        existing_encoding_char = session.query(CodePoint).filter(CodePoint.char == char and CodePoint.encoding_standard_id == encoding_type.id).first()

        if(existing_encoding_char is None):
            encoding_type.charset.append(CodePoint(char, encoded_char))
        else:
            existing_encoding_char.encoded_char = encoded_char

    session.add(encoding_type)
    session.commit()

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding type updated successfully"})