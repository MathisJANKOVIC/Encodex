from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.models import EncodingStandard
from database.connection import LocalSession

class EncodeString(BaseModel):
    encoding_standard_name: str = Field(..., description="Name of the encoding standard to use", example="ASCII-hexa")
    string: str = Field(..., description="String to encode", example="This a string to encode")

router = APIRouter()

@router.post("/encoding-standard/encode")
def encode_string(body: EncodeString = Body(...)):

    with LocalSession() as session:
        try:
            encoding_standard: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == body.encoding_standard_name).first()
        except SQLAlchemyError:
            return JSONResponse(status_code=500, detail="An error occured with the database")

        if(encoding_standard is None):
            raise HTTPException(status_code=404, detail="Encoding standard not found")

        encoded_string = ""
        for i, char in enumerate(body.string):
            if(not encoding_standard.case_sensitive):
                char = char.lower()

            encoded_char = encoding_standard.encode(char)

            if(encoded_char is None):
                if(encoding_standard.allowed_unrefenced_chars):
                    encoded_string += char
                else:
                    raise HTTPException(status_code=422, detail=f"Failed to encode character '{char}'")
            else:
                encoded_string += encoded_char

            if(i+1 < len(body.string)):
                encoded_string += encoding_standard.encoded_char_sep

    return JSONResponse(status_code=200, content={"encoded_string": encoded_string})