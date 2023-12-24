from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingStandard

class BodyModel(BaseModel):
    encoding_standard_name: str
    encoded_string: str

router = APIRouter()

@router.post("/encodex/decode/")
def decode_string(body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_standard: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == body.encoding_standard_name).first()

    if(encoding_standard is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Character encoding standard not found"})

    if(not encoding_standard.case_sensitive):
        body.encoded_string = body.encoded_string.lower()

    decoded_string = ""

    if(encoding_standard.encoded_char_sep):
        encoded_chars = body.encoded_string.split(encoding_standard.encoded_char_sep)
    else:
        encoded_chars = [
            body.encoded_string[i:i + encoding_standard.encoded_char_len]
            for i in range(0, len(body.encoded_string), encoding_standard.encoded_char_len)
        ]

    for encoded_char in encoded_chars:
        decoded_char = encoding_standard.decode(encoded_char)

        if(decoded_char is None):
            if(encoding_standard.allowed_unrefenced_chars):
                decoded_string += encoded_char
            else:
                session.close()
                return JSONResponse(status_code=400, content={"succes": False, "message": f"Could not decode {encoded_char}"})
        else:
            decoded_string += decoded_char

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": decoded_string})
