from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingType

router = APIRouter()

@router.get("/encodex/{encoding_type_name}")
def get(encoding_type_name: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    encoding_type = {
        "id": encoding_type.id,
        "name": encoding_type.name,
        "encoding_chars": {encoding_char.char: encoding_char.encoded_char for encoding_char in encoding_type.encoding_chars}
    }

    session.close()
    return JSONResponse(status_code=200, content = {"succes": True, "content": encoding_type})
