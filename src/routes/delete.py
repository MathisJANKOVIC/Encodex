from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from database.connection import LocalSession
from database.models import EncodingStandard

router = APIRouter()

@router.delete("/encodex/delete/{encoding_type_name}")
def delete_encoding_standard(encoding_type_name: str):

    with LocalSession() as session:
        try:
            encoding_standard = session.query(EncodingStandard).filter(EncodingStandard.name == encoding_type_name)

            if(encoding_standard is None):
                raise HTTPException(status_code=404, detail="Encoding standard not found")

            session.delete(encoding_standard)
            session.commit()

        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="An error occured with the database")

    return JSONResponse(status_code=200, content={"detail": f"Encoding standard '{encoding_type_name}' deleted successfully"})