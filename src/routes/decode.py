from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.connection import LocalSession
from database.models import EncodingStandard

class DecodeString(BaseModel):
    encoding_standard_name: str = Field(..., description="Name of the encoding standard to use", example="ASCII-hexa")
    encoded_string: str = Field(..., description="String encoded with the encoding standard", example="54 68 69 73 20 61 20 73 74 72 69 6E 67 20 74 6F 20 64 65 63 6F 64 65")

router = APIRouter()

@router.post("/encoding-standard/decode")
def decode_string(body: DecodeString = Body(...)):

    with LocalSession() as session:
        try:
            encoding_standard: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == body.encoding_standard_name).first()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

        if(encoding_standard is None):
            raise HTTPException(status_code=404, detail="Encoding standard not found")

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
                    raise HTTPException(status_code=422, detail=f"Failed to decode '{encoded_char}'")
            else:
                decoded_string += decoded_char

    return JSONResponse(status_code=200, content={"decoded_string": decoded_string})
