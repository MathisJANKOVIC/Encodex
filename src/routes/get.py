from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.models import EncodingStandard
from database.connection import LocalSession

router = APIRouter()

@router.get("/encodex/")
def get_all_encoding_types():

    session = LocalSession()
    encoding_types: list[EncodingStandard] = session.query(EncodingStandard).all()

    encoding_types_dict = [encoding_type.dict() for encoding_type in encoding_types]

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": encoding_types_dict})

@router.get("/encodex/{encoding_type_name}")
def get_encoding_type(encoding_type_name: str):

    session = LocalSession()
    encoding_type = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    encoding_type_dict = encoding_type.dict()

    session.close()
    return JSONResponse(status_code=200, content = {"succes": True, "content": encoding_type_dict})