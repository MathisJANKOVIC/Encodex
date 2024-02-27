from fastapi import FastAPI
import routes

app = FastAPI()

app.include_router(routes.get_standards.router)

app.include_router(routes.encode.router)

app.include_router(routes.decode.router)

app.include_router(routes.create_standard.router)

app.include_router(routes.update_standard_charset.router)

app.include_router(routes.delete_standard.router)

app.include_router(routes.rename_standard.router)