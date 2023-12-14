from fastapi import FastAPI
import routes

app = FastAPI()

app.include_router(routes.get.router)

app.include_router(routes.encode.router)

app.include_router(routes.decode.router)

app.include_router(routes.create.router)

app.include_router(routes.update.router)

app.include_router(routes.delete.router)