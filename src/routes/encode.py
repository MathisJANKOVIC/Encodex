from pydantic import BaseModel
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingType
from database.connection import LocalSession

class BodyModel(BaseModel):
    string: str

router = APIRouter()

@router.post("/encodex/{encoding_type_name}/encode/")
def encode_string(encoding_type_name: str, body: BodyModel = Body(...)):

    session = LocalSession()
    encoding_type: EncodingType = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    encoded_string = ""
    for i, char in enumerate(body.string):
        if(not encoding_type.is_case_sensitive):
            char = char.lower()

        if(char == " "):
            encoded_string = encoded_string + encoding_type.encoded_words_sep
        else:
            encoded_string = encoded_string + encoding_type.encoded_char(char)

            if(i+1 < len(body.string) and body.string[i+1] != " "): # If the next character is not a space or the last character
                encoded_string = encoded_string + encoding_type.encoded_chars_sep

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": encoded_string})