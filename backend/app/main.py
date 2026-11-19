from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import partidas
from app.routers import estatisticas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(partidas.router)
app.include_router(estatisticas.router)
