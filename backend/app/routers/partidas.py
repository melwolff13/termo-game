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


@router.post("/{id}/tentativa", response_model=TentativaResponse, status_code=200)
def post_tentativa(partida_id: int, body: EnviarTentativaRequest, db=Depends(get_db)):
    #1 buscar a partida no banco de dados
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if partida is None:
        raise HTTPException(status_code=404, detail="Partida não encontrada")

    #2 receber tentativa/jogada
    try:
        resultado = controlar_jogada(partida = partida, jogada = body.jogada.upper(), db = db)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))

    #3 exibir ou nao a palavra secreta
    palavra_revelada = None
    if resultado["status"] != StatusPartida.EM_ANDAMENTO:
        palavra_revelada = partida.palavra_secreta.palavra

    return TentativaResponse(
        jogada = resultado["jogada"],
        resultado = resultado["resultado"],
        tentativas_usadas = resultado["tentativas_usadas"],
        tentativas_restantes = 6 - resultado["tentativas_usadas"],
        status = resultado["status"],
        palavra_secreta = palavra_revelada
    )
        
