from fastapi import FastAPI, HTTPException, Body

from database.models import EncodingCharacter, EncodingType
from database.connection import LocalSession

app = FastAPI()

@app.get("/encodex/")
def get_all():
    pass

@app.get("/encodex/{encoding_name}")
def get(encoding_name: str):
    pass

@app.get("/encodex/{encoding_name}/encode/{sequence}")
def encode(encoding_name: str, sequence: str):
    pass

@app.get("/encodex/{encoding_name}/decode/{sequence}")
def decode(encoding_name: str, sequence: str):
    pass

@app.patch("/encodex/{encoding_name}/update/")
def update(encoding_name: str, new_encoding_format: dict = Body(...)):
    pass

@app.delete("/encodex/{encoding_type_name}/delete/", status_code=200)
def delete(encoding_type_name: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        raise HTTPException(status_code=404, detail={"succes": False, "message": "Encoding type not found"})

    session.query(EncodingCharacter).filter(EncodingCharacter.id_encoding_type == encoding_type.id).delete()
    session.delete(encoding_type)

    session.commit()
    session.close()

    return {"succes": True, "message": "Encoding type deleted successfully"}

@app.post("/encodex/create/{encoding_type_name}", status_code=201)
def create(encoding_type_name: str, encoding_characters: dict = Body(...)):

    session = LocalSession()

    if(session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first() is not None):
        session.close()
        raise HTTPException(status_code=400, detail={"Succes": False, "message": "Encoding type already exists"})

    session.add(EncodingType(encoding_type_name, encoding_characters))
    session.commit()

    session.close()
    return {"succes": True, "message": "Encoding type created successfully"}