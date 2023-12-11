from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingType

router = APIRouter()

@router.get("/encodex/")
def get_all():

    session = LocalSession()
    encoding_types = session.query(EncodingType).all()

    encoding_types = [{
            "id": encoding_type.id,
            "name": encoding_type.name,
            "encoding_chars": {encoding_char.char: encoding_char.encoded_char for encoding_char in encoding_type.encoding_chars}
        } for encoding_type in encoding_types
    ]

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "content": encoding_types})