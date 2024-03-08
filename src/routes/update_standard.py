from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field

from database.connection import LocalSession
from database.models import EncodingStandard, CodePoint

class UpdateEncodingStandard(BaseModel):
    encoding_standard_id: int = Field(..., description = "Id of the encoding standard.")
    charset: dict[str, str] = Field(...,
        description = """Dictionary mapping characters to their encoded representations to add in the encoding standard.
        If a character already exists in the charset, its encoded representation will be updated."""
    )

router = APIRouter()

@router.patch("/encoding-standard/update-charset")
def update_encoding_standard_charset(body: UpdateEncodingStandard = Body(...)):

    with LocalSession() as session:
        try:
            standard = EncodingStandard.get(session, body.encoding_standard_id)

            if(standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            for char, encoded_char in body.charset.items():
                if(standard.is_encoded_char_used_by_another_char(char, encoded_char)):
                    raise HTTPException(
                        status_code = 422,
                        detail = f"Encoded character '{encoded_char}' is not unique in the encoding standard charset"
                    )

                if(len(char) != 1):
                    raise HTTPException(status_code=422, detail="Characters in charset must be one character long")

                if(encoded_char == ""):
                    raise HTTPException(status_code=422, detail="Encoded characters in charset cannot be empty")

                if(len(encoded_char) != standard.encoded_char_len and standard.encoded_char_len is not None):
                    raise HTTPException(
                        status_code = 422,
                        detail = "Encoded characters lenght in charset must be the same as defined in character encoding standard"
                    )

                if(standard.encoded_char_sep in encoded_char and standard.encoded_char_sep != ""):
                    raise HTTPException(status_code=422, detail="Encoded characters in charset cannot contain character separator")

                same_existing_char = standard.code_point(char)

                if(same_existing_char is None):
                    standard.charset.append(CodePoint(char, encoded_char))
                else:
                    same_existing_char.encoded_char = encoded_char

                session.add(standard)
                session.commit()

                standard_dict = standard.dict()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"detail": "Encoding standard updated successfully", "encoding_standard": standard_dict})