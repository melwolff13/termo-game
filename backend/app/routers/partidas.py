from app.models import *
from app.schemas.partida import *
from app.services.jogo import *
from fastapi import APIRouter, Depends, HTTPException
from app.database import *

router = APIRouter(
    prefix="/partidas",
    tags=["partidas"]
)

@router.post("/", response_model=PartidaResponse, status_code=201)
def post_criar_partida(body: CriarPartidaRequest, db=Depends(get_db)):
    
    try:
        partida = criar_partida(body.jogador_id, db)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))

    return PartidaResponse(
        partida_id = partida.id, 
        jogador_id = partida.jogador_id, 
        status = partida.status,
        qtd_tentativas = partida.qtd_tentativas,
        tentativas_restantes = 6-partida.qtd_tentativas
    )

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
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))
        
