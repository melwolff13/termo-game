from app.models import *
from app.schemas.partida import *
from app.services.jogo import *
from fastapi import APIRouter, Depends, HTTPException
from app.database import *
from sqlalchemy import select, func, desc

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
def get_partida(partida_id:int, db=Depends(get_db)):

    partida = db.query(Partida).filter(Partida.id == partida_id).first()

    if partida is None:
        raise HTTPException(status_code=404,detail="Partida não encontrada")

    palavra_revelada = None
    if partida.status != StatusPartida.EM_ANDAMENTO:
        palavra_revelada = partida.palavra_secreta.palavra

    return EstadoPartidaResponse(
        tentativas_usadas = partida.qtd_tentativas,
        tentativas_restantes = 6 - partida.qtd_tentativas,
        status =  partida.status,
        palavra_secreta = palavra_revelada
    )


@router.post("/{partida_id}/tentativa", response_model=TentativaResponse, status_code=200)
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
        
@router.get("/{jogador_id}/estatistica", response_model=EstatisticaResponse, status_code=200)
def estatistica_jogador(jogador_id: str, db=Depends(get_db)):

    #1 consulta a quantidade de partidas pelo id do jogador
    qtd_partida = db.scalar(
        select(func.count())
        .select_from(Partida)
        .filter(Partida.jogador_id == jogador_id)
        )
    
    qtd_vitoria = db.scalar(
        select(func.count())
        .select_from(Partida)
        .filter(Partida.jogador_id == jogador_id, Partida.status == StatusPartida.VENCEU)
        )

    consulta = (
        select(Partida)
        .where(Partida.jogador_id == jogador_id)
        .order_by(desc(Partida.id))
        )

    partidas = db.scalars(consulta).all()

    sequencia_atual = 0

    for partida in partidas:
        if partida.status == StatusPartida.VENCEU:
            sequencia_atual += 1
        else:
            break

    sequencias = set()
    contagem_sequencia = 0
    maior_sequencia = 0

    for partida in partidas:
        if partida.status == StatusPartida.VENCEU:
            contagem_sequencia += 1
        else:
            sequencias.add(contagem_sequencia)
            contagem_sequencia = 0

    sequencias.add(contagem_sequencia)
    maior_sequencia = max(sequencias)

    return EstatisticaResponse(
        qtd_partidas = qtd_partida,
        qtd_vitorias = qtd_vitoria,
        sequencia_atual= sequencia_atual,
        maior_sequencia= maior_sequencia
        
    )
