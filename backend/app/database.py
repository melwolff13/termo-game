from sqlalchemy import create_engine #conexão com o banco de dados
from sqlalchemy.orm import sessionmaker, DeclarativeBase #Cria a sessão local/interação 
from dotenv import load_dotenv #.env
import os

load_dotenv() #ALOCAR .EVN NA MEMORIA
conexao = create_engine(os.getenv("DATABASE_URL")) #CARREGAR LINK DO BD DO ARQUIVO .ENV ALOCADO NA MEMORIA
SessionLocal = sessionmaker(bind=conexao,autocommit=False,autoflush=False) #não faz nada automatico

class Base(DeclarativeBase):#pai dos models
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db #passar o bd para a rota
    finally:
        db.close() #fechar a sessão com o bd