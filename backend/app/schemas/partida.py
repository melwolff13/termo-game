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

class TentativaResponse(BaseModel): # usado no get /partidas/{partida_id} (EstadoPartidaResponse)
    jogada: str
    resultado: List[Literal["verde", "amarelo", "cinza"]]

class ResultadoTentativaResponse(BaseModel): # retorno do post /partidas/{partida_id}/tentativa
    jogada: str
    resultado: list[str]
    tentativas_usadas: int
    tentativas_restantes: int
    status: StatusPartida
    palavra_secreta: str | None = None

class EstadoPartidaRequest(BaseModel):
    partida_id: str

class EstadoPartidaResponse(BaseModel):
    id: int
    status: StatusPartida
    tentativas_usadas: int
    tentativas_restantes: int
    tentativas: list[TentativaResponse]
    palavra_secreta: str | None = None

class EstatisticaRequest(BaseModel):
    jogador_id: str

class EstatisticaResponse(BaseModel):
    qtd_partidas: int
    qtd_vitorias: int
    sequencia_atual: int
    maior_sequencia: int

