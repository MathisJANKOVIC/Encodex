from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from database.models import EncodingType, EncodingChar
from database.connection import LocalSession

router = APIRouter()

@router.patch("/encodex/{encoding_type_name}/update/")
def update(encoding_type_name: str, new_encoding_chars: dict = Body(...)):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    for char, encoding_char in new_encoding_chars.items():
        encoding_type.encoding_chars.append(EncodingChar(char, encoding_char))

    session.add(encoding_type)
    session.commit()

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding type updated successfully"})