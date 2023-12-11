from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.models import EncodingType, EncodingChar
from database.connection import LocalSession

router = APIRouter()

@router.get("/encodex/{encoding_type_name}/encode/{sequence}", status_code=200)
def encode(encoding_type_name: str, sequence: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    encoding_chars: list[EncodingChar] = encoding_type.encoding_chars
    session.close()

    encoded_sequence = ""
    for char in sequence:
        for encoding_char in encoding_chars:
            if(encoding_char.char == char):
                encoded_sequence = encoded_sequence + encoding_char.encoded_char
                break
        else:
            encoded_sequence = encoded_sequence + char

    return JSONResponse(status_code=200, content = {"succes": True, "content": encoded_sequence})