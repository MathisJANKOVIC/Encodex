from fastapi import FastAPI, HTTPException, Body

from database.models import EncodingType
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

@app.delete("/encodex/{encoding_name}/delete/")
def delete(encoding_name: str):
    pass

@app.post("/encodex/create/{encoding_type_name}", status_code=201)
def create(encoding_type_name: str, encoding_characters: dict = Body(...)):

    session = LocalSession()

    if(session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first() is not None):
        session.close()
        raise HTTPException(status_code=400, detail={"Succes": False, "message": "Encoding type already exists"})

    session.add(EncodingType(encoding_type_name, encoding_characters))
    session.commit()

    return {"Succes": True, "message": "Encoding type created successfully"}