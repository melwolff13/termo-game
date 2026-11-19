from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partida import EstatisticaResponse
from app.services.jogo import calcular_estatisticas

router = APIRouter(
    prefix="/stats",
    tags=["estatísticas"]
)

@router.get("/{jogador_id}", response_model=EstatisticaResponse)
def get_estatistica_jogador(jogador_id: str, db: Session = Depends(get_db)):
    return calcular_estatisticas(jogador_id, db)