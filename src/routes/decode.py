from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingType
from database.connection import LocalSession

class BodyModel(BaseModel):
    encoded_string: str

router = APIRouter()

@router.post("/encodex/{encoding_type_name}/decode/")
def decode_string(encoding_type_name: str, body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_type: EncodingType = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    decoded_str = buffer = ""

    if(encoding_type.encoded_chars_len is None):
        for encoded_char in body.encoded_string:
            if(encoded_char == encoding_type.encoded_words_sep):
                decoded_str = decoded_str + encoding_type.decoded_char(buffer) + " "
                buffer = ""
            elif(encoded_char == encoding_type.encoded_chars_sep):
                decoded_str = decoded_str + encoding_type.decoded_char(buffer)
                buffer = ""
            else:
                buffer = buffer + encoded_char

        decoded_str = decoded_str + encoding_type.decoded_char(buffer)
    else:
        for encoded_char in body.encoded_string :
            if(encoded_char == encoding_type.encoded_words_sep):
                decoded_str = decoded_str + encoding_type.decoded_char(buffer) + " "
                buffer = ""
            elif(encoded_char == encoding_type.encoded_chars_sep):
                decoded_str = decoded_str + encoding_type.decoded_char(buffer)
                buffer = ""
            else:
                buffer = buffer + encoded_char
                if(len(buffer) == encoding_type.encoded_chars_len):
                    decoded_str = decoded_str + encoding_type.decoded_char(buffer)
                    buffer = ""

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": decoded_str})
