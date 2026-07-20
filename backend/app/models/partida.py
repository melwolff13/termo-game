from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, func
import enum
from sqlalchemy.orm import relationship
from app.database import Base


class StatusPartida(str, enum.Enum):
    EM_ANDAMENTO = "em_andamento"
    VENCEU = "venceu"
    PERDEU = "perdeu"

class Partida(Base):
    __tablename__ = "partidas"
    id = Column(Integer, primary_key=True, index=True)
    jogador_id = Column(String, nullable=False, index=True)
    palavra_secreta_id = Column(Integer, ForeignKey("palavras.id"),nullable=False)
    status = Column(Enum(StatusPartida), default=StatusPartida.EM_ANDAMENTO, nullable=False, )
    tentativas = Column(Integer, nullable=False)
    iniciada_em = Column(DateTime, server_default=func.now(), nullable=False)
    finalizada_em = Column(DateTime, nullable=False)

    palavra_secreta = relationship("Palavra")
    tentativas = relationship("Tentativa",back_populates="partida")