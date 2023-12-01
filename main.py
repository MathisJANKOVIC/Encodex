from fastapi import FastAPI

app = FastAPI()

@app.get("/encoding")
def get_all():
    pass

@app.get("/encoding/{encoding_name}")
def get(encoding_name: str):
    pass

@app.get("/encoding/{encoding_name}/encode/{sequence}")
def encode(encoding_name: str, sequence: str):
    pass

@app.get("/encoding/{encoding_name}/decode/{sequence}")
def decode(encoding_name: str, sequence: str):
    pass

@app.patch("/encoding/{encoding_name}/update/{new_encoding_format}")
def update(encoding_name: str, new_encoding_format: dict):
    pass

@app.delete("/encoding/{encoding_name}/delete/")
def delete(encoding_name: str):
    pass

@app.post("/encoding/create/{encoding_name}")
def create(encoding_name: str):
    pass
