from fastapi import FastAPI
from app.routers import partidas

app = FastAPI()

app.include_router(partidas.router)
