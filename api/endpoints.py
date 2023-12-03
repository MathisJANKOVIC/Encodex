from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/codex/")
def get_all():
    pass

@app.get("/codex/{encoding_name}")
def get(encoding_name: str):
    pass

@app.get("/codex/{encoding_name}/encode/{sequence}")
def encode(encoding_name: str, sequence: str):
    pass

@app.get("/codex/{encoding_name}/decode/{sequence}")
def decode(encoding_name: str, sequence: str):
    pass

@app.patch("/codex/{encoding_name}/update/")
def update(encoding_name: str, new_encoding_format: dict = Body(...)):
    pass

@app.delete("/codex/{encoding_name}/delete/")
def delete(encoding_name: str):
    pass

@app.post("/codex/create/{encoding_name}")
def create(encoding_name: str):
    pass
