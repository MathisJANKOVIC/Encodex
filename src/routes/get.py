from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.models import EncodingStandard
from database.connection import LocalSession

router = APIRouter()

@router.get("/encodex/")
def get_all_encoding_standards():

    session = LocalSession()
    encoding_standard: list[EncodingStandard] = session.query(EncodingStandard).all()

    encoding_standard_dict = [encoding_type.dict() for encoding_type in encoding_standard]

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": encoding_standard_dict})

@router.get("/encodex/{encoding_type_name}")
def get_encoding_standard(encoding_type_name: str):

    session = LocalSession()
    encoding_standard = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name).first()

    if(encoding_standard is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Character encoding standard not found"})

    encoding_standard_dict = encoding_standard.dict()

    session.close()
    return JSONResponse(status_code=200, content = {"succes": True, "content": encoding_standard_dict})