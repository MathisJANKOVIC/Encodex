from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.connection import LocalSession
from database.models import EncodingStandard, CodePoint

class UpdateEncodingStandard(BaseModel):
    encoding_standard_name: str = Field(...,
        description = "Name of the encoding standard to update",
        example = "ISO-8859-8"
    )
    encoding_chars: dict = Field(...,
        description = "Dictionary mapping characters to their encoded representations to add or replace in the encoding standard",
        example = {"a": "A", "b": "B", "c": "C"}
    )

router = APIRouter()

@router.patch("/encodex/update/")
def update_encoding_standard(body: UpdateEncodingStandard = Body(...)):

    with LocalSession() as session:
        try:
            encoding_standard: EncodingStandard = session.query(EncodingStandard).filter(EncodingStandard.name == body.encoding_standard_name ).first()

            if(encoding_standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            for char, encoded_char in body.encoding_chars.items():
                if(encoded_char in encoding_standard.dict["charset"].values()):
                    raise HTTPException(status_code=422, detail="Encoded characters must be unique")

                if(len(char) != 1):
                    raise HTTPException(status_code=422, detail="Characters must be one character long")

                if(encoded_char == ""):
                    raise HTTPException(status_code=422, detail="Encoded characters cannot be empty")

                if(len(encoded_char) != encoding_standard.encoded_char_len and encoding_standard.encoded_char_len is not None):
                    raise HTTPException(status_code=422, detail="Encoded characters lenght must be the same as defined in character encoding standard")

                if(encoding_standard.encoded_char_sep in encoded_char):
                    raise HTTPException(status_code=422, detail="Encoded characters cannot contain character separator")

                similar_existing_char = session.query(CodePoint).filter(CodePoint.char == char and CodePoint.encoding_standard_id == encoding_standard.id).first()

                if(similar_existing_char is None):
                    encoding_standard.charset.append(CodePoint(char, encoded_char))
                else:
                    similar_existing_char.encoded_char = encoded_char

                session.add(encoding_standard)
                session.commit()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An unexpected error has occured with the database")

    return JSONResponse(status_code=200, content={"detail": f"Encoding standard '{encoding_standard.name}' updated successfully"})