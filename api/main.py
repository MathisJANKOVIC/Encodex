from fastapi import FastAPI
from . import routes

app = FastAPI()

app.include_router(routes.get_type.router)

app.include_router(routes.get_all_types.router)

app.include_router(routes.encode.router)

app.include_router(routes.create_type.router)

app.include_router(routes.delete_type.router)

app.include_router(routes.add_char.router)
