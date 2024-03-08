from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from database.connection import LocalSession
from database.models import EncodingStandard

class RenameEncodingStandard(BaseModel):
    encoding_standard_id: int
    new_name: str

router = APIRouter()

@router.put("/encoding-standard/rename")
def rename_encoding_standard(body: RenameEncodingStandard = Body(...)):
    with LocalSession() as session:
        try:
            standard = EncodingStandard.get(session, body.encoding_standard_id)

            if(standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            if(EncodingStandard.get(session, name=body.new_name) is not None):
                raise HTTPException(status_code=422, detail="An encoding standard with this name already exists")

            standard.name = body.new_name

            session.add(standard)
            session.commit()

            standard_dict = standard.dict()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"detail": "Encoding standard renamed successfully", "encoding_standard": standard_dict})