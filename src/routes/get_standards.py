from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.models import EncodingStandard
from database.connection import LocalSession

router = APIRouter()

@router.get("/encoding-standard")
def get_all_encoding_standards():

    with LocalSession() as session:
        try:
            standards: list[EncodingStandard] = EncodingStandard.get(session)
            standards_dict = [standard.dict for standard in standards]
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"content": standards_dict})

@router.get("/encoding-standard/{encoding_standard_id}")
def get_encoding_standard(encoding_standard_id: int):

    with LocalSession() as session:
        try:
            standard = EncodingStandard.get(session, id=encoding_standard_id)

            if(standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            standard_dict = standard.dict
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"content": standard_dict})