from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Tentativa(Base):
    __tablename__ = "tentativas"
    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"), index=True, nullable=False)
    jogada = Column(String(5), nullable=False)
    resultado = Column(JSON, nullable=False)
    data = Column(DateTime, server_default=func.now(), nullable=False)

    partida = relationship("Partida", back_populates="tentativas")




