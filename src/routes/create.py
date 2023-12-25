from math import e
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.models import EncodingStandard
from database.connection import LocalSession

class CreateEncodingStandard(BaseModel):
    name: str = Field(...,
        description = "Name of the encoding standard",
        example = "Maj"
    )
    case_sensitive: bool = Field(...,
        description = "Whether the encoding standard is case sensitive or not, if true, 'a' and 'A' will be treated as different characters",
        example = True
    )
    allowed_unrefenced_chars: bool = Field(...,
        description = "Behavior when a character is not defined in the encoding standard while encoding or decoding. If true, the character will be kept, if false, an exception will be raised",
        example = True
    )
    encoded_char_len: int | None = Field(None,
        description = "Length of all encoded characters. If null, encoded characters won't have a fixed length.",
        example = 1
    )
    encoded_char_sep: str = Field(...,
        description="Separator of the encoded characters. Can be empty only if 'encoded_char_len' is defined.",
        example = " "
    )
    charset: dict[str, str] = Field(...,
        description="Dictionary mapping characters to their encoded representations.",
        example = {"a": "A", "b": "B", "c": "C"}
    )

router = APIRouter()

@router.post("/encodex/create/")
def create_encoding_standard(encoding_standard: CreateEncodingStandard = Body(...)):

    with LocalSession() as session:
        try:
            if(session.query(EncodingStandard).filter(EncodingStandard.name == encoding_standard.name).first() is not None):
                raise HTTPException(status_code=409, detail=f"Encoding standard '{encoding_standard.name}' already exists")
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An unexpected error has occured with the database")

        if(len(encoding_standard.name) < 3):
            raise HTTPException(status_code=422, detail="Encoding standard name cannot have less than 3 characters")

        if(len(encoding_standard.name) > 32):
            raise HTTPException(status_code=422, detail="Encoding standard name cannot have more than 32 characters")

        if(not encoding_standard.name.replace(" ","").replace("-","").replace("_","").isalnum()):
            raise HTTPException(status_code=422, detail="Encoding standard name cannot contain special characters")

        if(len(encoding_standard.charset.values()) != len(set(encoding_standard.charset.values()))):
            raise HTTPException(status_code=422, detail="Encoded characters must be unique")

        if(encoding_standard.encoded_char_len is None and encoding_standard.encoded_char_sep == ""):
            raise HTTPException(status_code=422, detail="encoded_char_len and encoded_char_sep cannot be both undefined or empty for an encoding standard")

        if(not encoding_standard.case_sensitive):
            encoding_standard.charset = {char.lower(): encoded_char for char, encoded_char in encoding_standard.charset.items()}

        for char, encoded_char in encoding_standard.charset.items():
            if(len(char) != 1):
                raise HTTPException(status_code=422, detail="Characters must be one character long")

            if(encoding_standard.encoded_char_len is None):
                if(encoded_char == ""):
                    raise HTTPException(status_code=422, detail="Encoded characters cannot be empty")
            elif(len(encoded_char) != encoding_standard.encoded_char_len):
                raise HTTPException(status_code=422, detail="Encoded characters lenght must be the same as defined in encoding standard")

            if(encoding_standard.encoded_char_sep != "" and encoding_standard.encoded_char_sep in encoded_char):
                raise HTTPException(status_code=422, detail="Encoded characters cannot contain character separator")

        session.add(EncodingStandard(
            name = encoding_standard.name,
            case_sensitive = encoding_standard.case_sensitive,
            allowed_unrefenced_chars = encoding_standard.allowed_unrefenced_chars,
            encoded_char_len = encoding_standard.encoded_char_len,
            encoded_char_sep = encoding_standard.encoded_char_sep,
            charset = encoding_standard.charset
        ))

        session.commit()
    raise JSONResponse(status_code=201, content="Encoding standard created successfully")