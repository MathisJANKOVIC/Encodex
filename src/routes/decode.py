from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field

from database.connection import LocalSession
from database.models import EncodingStandard

class DecodeString(BaseModel):
    encoding_standard_id: str = Field(..., description="Id of the encoding standard to use")
    encoded_string: str = Field(..., description="String to decode")

router = APIRouter()

@router.post("/encoding-standard/decode")
def decode_string(body: DecodeString = Body(...)):

    with LocalSession() as session:
        try:
            standard = EncodingStandard.get(session, body.encoding_standard_id)

            if(standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            if(not standard.case_sensitive):
                body.encoded_string = body.encoded_string.lower()

            decoded_string = ""

            if(standard.encoded_char_sep):
                encoded_chars = body.encoded_string.split(standard.encoded_char_sep)
            else:
                encoded_chars = [
                    body.encoded_string[i:i + standard.encoded_char_len]
                    for i in range(0, len(body.encoded_string), standard.encoded_char_len)
                ]

            for encoded_char in encoded_chars:
                decoded_char = standard.decode(encoded_char)

                if(decoded_char is None):
                    if(standard.allowed_unrefenced_chars):
                        decoded_string += encoded_char
                    else:
                        raise HTTPException(status_code=422, detail=f"Failed to decode '{encoded_char}'")
                else:
                    decoded_string += decoded_char

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"decoded_string": decoded_string})
