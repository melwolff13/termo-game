from app.models import *
from app.schemas.partida import *
from app.services.jogo import *
from fastapi import APIRouter, Depends
from app.database import *

router = APIRouter(
    prefix="/stats",
    tags=["estatísticas"]
)

@router.get("/{jogador_id}", response_model=EstatisticaResponse)
def get_estatistica_jogador(jogador_id: str, db: Session = Depends(get_db)):
    return calcular_estatisticas(jogador_id, db)