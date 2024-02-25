from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.connection import LocalSession
from database.models import EncodingStandard, CodePoint

router = APIRouter()

@router.delete("/encoding-standard/delete/{encoding_type_name}")
def delete_encoding_standard(encoding_type_name: str):

    with LocalSession() as session:
        try:
            encoding_standard = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name).first()

            if(encoding_standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            session.query(CodePoint).filter(CodePoint.encoding_standard_id == encoding_standard.id).delete()
            session.delete(encoding_standard)
            session.commit()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An unexpected error has occured with the database")

    return JSONResponse(status_code=200, content={"detail": f"Encoding standard '{encoding_type_name}' deleted successfully"})