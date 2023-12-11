from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingType, EncodingChar

router = APIRouter()

@router.delete("/encodex/{encoding_type_name}/delete/")
def main(encoding_type_name: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    session.query(EncodingChar).filter(EncodingChar.encoding_type_id == encoding_type.id).delete()
    session.delete(encoding_type)

    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding type deleted successfully"})