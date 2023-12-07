from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from database.connection import LocalSession
from database.models import EncodingCharacter, EncodingType

app = FastAPI()

@app.get("/encodex/")
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

@app.get("/encodex/{encoding_type_name}")
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

@app.get("/encodex/{encoding_type_name}/encode/{sequence}", status_code=200)
def encode(encoding_type_name: str, sequence: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    encoding_chars: list[EncodingCharacter] = encoding_type.encoding_chars
    session.close()

    encoded_sequence = ""
    for char in sequence:
        for encoding_char in encoding_chars:
            if(encoding_char.char == char):
                encoded_sequence = encoded_sequence + encoding_char.encoded_char
                break
        else:
            encoded_sequence = encoded_sequence + char

    return JSONResponse(status_code=200, content = {"succes": True, "content": encoded_sequence})

@app.patch("/encodex/{encoding_type_name}/update/")
def update(encoding_type_name: str, new_encoding_chars: dict = Body(...)):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    for char, encoding_char in new_encoding_chars.items():
        encoding_type.encoding_chars.append(EncodingCharacter(char, encoding_char))

    session.add(encoding_type)
    session.commit()

    session.close()
    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding type updated successfully"})

@app.delete("/encodex/{encoding_type_name}/delete/")
def delete(encoding_type_name: str):

    session = LocalSession()
    encoding_type = session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first()

    if(encoding_type is None):
        session.close()
        return JSONResponse(status_code=404, content={"succes": False, "message": "Encoding type not found"})

    session.query(EncodingCharacter).filter(EncodingCharacter.id_encoding_type == encoding_type.id).delete()
    session.delete(encoding_type)

    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={"succes": True, "message": "Encoding type deleted successfully"})

@app.post("/encodex/create/{encoding_type_name}")
def create(encoding_type_name: str, encoding_characters: dict = Body(...)):

    session = LocalSession()

    if(session.query(EncodingType).filter(EncodingType.name == encoding_type_name).first() is not None):
        session.close()
        return JSONResponse(status_code=400, detail={"Succes": False, "message": "Encoding type already exists"})

    session.add(EncodingType(encoding_type_name, encoding_characters))
    session.commit()

    session.close()
    return JSONResponse(status_code=201, content={"succes": True, "message": "Encoding type created successfully"})