from pydantic import BaseModel
from app.models.partida import StatusPartida

class CriarPartidaRequest(BaseModel):
    jogador_id: str

class PartidaResponse(BaseModel):
    partida_id: int
    jogador_id: str
    status: StatusPartida
    qtd_tentativas: int
    tentativas_restantes: int