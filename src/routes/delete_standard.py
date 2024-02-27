from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.connection import LocalSession
from database.models import EncodingStandard

router = APIRouter()

@router.delete("/encoding-standard/delete/{encoding_standard_id}")
def delete_encoding_standard(encoding_standard_id: int):

    with LocalSession() as session:
        try:
            standard = EncodingStandard.get(session, encoding_standard_id)

            if(standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            standard.delete(session)
            session.commit()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"detail": "Encoding standard deleted successfully"})