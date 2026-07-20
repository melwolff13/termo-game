from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Palavra(Base):
    __tablename__ = "palavras"
    id = Column(Integer, primary_key=True, index=True)
    palavra = Column(String(5), nullable=False, unique=True)
    isAtivo = Column(Boolean, default=True)