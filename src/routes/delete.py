from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingStandard, CodePoint

router = APIRouter()

@router.delete("/encodex/delete/{encoding_type_name}")
def delete_encoding_standard(encoding_type_name: str):

    session = LocalSession()
    encoding_standard = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name).first()

    if(encoding_standard is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Character encoding standard not found"})

    session.query(CodePoint).filter(CodePoint.encoding_standard_id == encoding_standard.id).delete()
    session.delete(encoding_standard)

    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={"succes": True, "message": "Character encoding standard deleted successfully"})