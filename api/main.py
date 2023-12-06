from fastapi import FastAPI, Body

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

@app.post("/encodex/create/{encoding_name}")
def create(encoding_name: str):
    pass
