from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partida import (
    CriarPartidaRequest, PartidaResponse, EstadoPartidaResponse,
    EnviarTentativaRequest, ResultadoTentativaResponse,
)
from app.services.jogo import (
    criar_partida, consultar_partida, controlar_jogada, PartidaNaoEncontrada, TentativaInvalida, PartidaEncerrada
)

router = APIRouter(
    prefix="/partidas",
    tags=["partidas"]
)

@router.post("/", response_model=PartidaResponse, status_code=201)
def post_criar_partida(body: CriarPartidaRequest, db=Depends(get_db)):
    try:
        return criar_partida(body.jogador_id, db)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))

@router.get("/{partida_id}", response_model=EstadoPartidaResponse, status_code=200)
def get_partida(partida_id: int, db: Session = Depends(get_db)):
    try:
        estado = consultar_partida(partida_id, db)
    except PartidaNaoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))

    return estado

@router.post("/{partida_id}/tentativa", response_model=ResultadoTentativaResponse)
def post_tentativa(partida_id: int, body: EnviarTentativaRequest, db: Session = Depends(get_db)):
    try:
        return controlar_jogada(partida_id, body.jogada, db)
    except PartidaNaoEncontrada as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    except TentativaInvalida as erro:
        raise HTTPException(status_code=422, detail=str(erro))
    except PartidaEncerrada as erro:
        raise HTTPException(status_code=409, detail=str(erro))
        
