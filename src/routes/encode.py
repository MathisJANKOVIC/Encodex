from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingStandard
from database.connection import LocalSession

class BodyModel(BaseModel):
    encoding_standard_name: str
    string: str

router = APIRouter()

@router.post("/encodex/encode/")
def encode_string(body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_standard: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == body.encoding_standard_name).first()

    if(encoding_standard is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Character encoding standard not found"})

    encoded_string = ""
    for i, char in enumerate(body.string):
        if(not encoding_standard.case_sensitive):
            char = char.lower()

        encoded_char = encoding_standard.encode(char)

        if(encoded_char is None):
            if(encoding_standard.allowed_unrefenced_chars):
                encoded_string = encoded_string + char
            else:
                session.close()
                return JSONResponse(status_code=422, content={"succes": False, "message": f"Coulnd't encode character `{char}`"})
        else:
            encoded_string = encoded_string + encoded_char

        if(i+1 < len(body.string)):
            encoded_string = encoded_string + encoding_standard.encoded_char_sep

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": encoded_string})