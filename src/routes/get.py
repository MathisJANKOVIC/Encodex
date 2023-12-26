from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.models import EncodingStandard
from database.connection import LocalSession

router = APIRouter()

@router.get("/encodex/")
def get_all_encoding_standards():

    with LocalSession() as session:
        try:
            encoding_standards: list[EncodingStandard] = session.query(EncodingStandard).all()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

        encoding_standards_dict = [encoding_standard.dict for encoding_standard in encoding_standards]

    return JSONResponse(status_code=200, content={"content": encoding_standards_dict})

@router.get("/encodex/{encoding_type_name}")
def get_encoding_standard(encoding_type_name: str):

    with LocalSession() as session:
        try:
            encoding_standard = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name).first()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

        if(encoding_standard is None):
            raise HTTPException(status_code=404, detail="Encoding standard not found")

        encoding_standard_dict = encoding_standard.dict

    return JSONResponse(status_code=200, content={"content": encoding_standard_dict})