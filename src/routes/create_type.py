from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingType
from database.connection import LocalSession

router = APIRouter()

@router.post("/encodex/create/{encoding_type_name}")
def create(encoding_type_name: str, encoding_characters: dict = Body(...)):

    session = LocalSession()

    if(session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first() is not None):
        session.close()
        return JSONResponse(status_code=400, detail={"Succes": False, "message": "Encoding type already exists"})

    session.add(EncodingType(encoding_type_name, encoding_characters))
    session.commit()

    session.close()
    return JSONResponse(status_code=201, content={"succes": True, "message": "Encoding type created successfully"})
