from pydantic import BaseModel
from typing import List, Literal
from app.models.partida import StatusPartida

class CriarPartidaRequest(BaseModel):
    jogador_id: str

class PartidaResponse(BaseModel):
    partida_id: int
    jogador_id: str
    status: StatusPartida
    qtd_tentativas: int
    tentativas_restantes: int

class EnviarTentativaRequest(BaseModel):
    jogada: str

class TentativaResponse(BaseModel):
    jogada: str
    resultado: List[Literal["verde", "amarelo", "cinza"]]
    tentativas_usadas: int
    tentativas_restantes: int
    status: StatusPartida
    palavra_secreta: str | None
