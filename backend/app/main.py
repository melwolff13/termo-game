from fastapi import FastAPI
from app.routers import partidas
from app.routers import estatisticas

app = FastAPI()

app.include_router(partidas.router)
app.include_router(estatisticas.router)
