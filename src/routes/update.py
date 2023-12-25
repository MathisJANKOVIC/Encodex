from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingStandard, CodePoint

class BodyModel(BaseModel):
    encoding_standard_name: str
    encoding_chars: dict

router = APIRouter()

@router.patch("/encodex/update/")
def update_encoding_standard(body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_standard: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == body.encoding_standard_name ).first()

    if(encoding_standard is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding standard not found"})

    for char, encoded_char in body.encoding_chars.items():
        if(encoded_char in encoding_standard.dict["charset"].values()):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters must be unique"})

        if(len(char) != 1):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Characters must be one character long"})

        if(len(encoded_char) == 0):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot be empty"})

        if(len(encoded_char) != encoding_standard.encoded_char_len and encoding_standard.encoded_char_len is not None):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters lenght must be the same as defined in character encoding standard"})

        if(encoding_standard.encoded_char_sep in encoded_char):
            session.close()
            return JSONResponse(status_code=422, content={"succes": False, "message": "Encoded characters cannot contain character separator"})

        similar_existing_char = session.query(CodePoint).filter(CodePoint.char == char and CodePoint.encoding_standard_id == encoding_standard.id).first()

        if(similar_existing_char is None):
            encoding_standard.charset.append(CodePoint(char, encoded_char))
        else:
            similar_existing_char.encoded_char = encoded_char

    session.add(encoding_standard)
    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding standard updated successfully"})