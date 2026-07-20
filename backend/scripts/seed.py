import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # basicamnete diz pro python procurar na raiz do projeto também
# quando você faz from app.db import SessionLocal, 
# o Python precisa encontrar a pasta app. 
# Mas esse script está dentro de scripts/, 
# então se você rodar python scripts/seed.py da raiz do projeto, 
# o Python não sabe que a pasta app existe no nível acima.
#sys.path = lista de pastas onde o python procura módulos
# __file__ = caminho do proprio arquivo (script/seed.py)
# __file__ -> scripts/seed.py
# os.path.dirname(__file__) -> scripts/
# os.path.dirname(os.path.dirname(__file__)) -> ./ (raiz)

from app.database import SessionLocal
from app.models import Palavra

PALAVRAS = [
    "carro", "porta", "livro", "campo", "banco",
    "cabra", "pedra", "terra", "fonte", "grito",
    "plano", "carta", "bolsa", "forca", "barco",
    "caldo", "bravo", "sopro", "virar", "prova",
    "tempo", "lugar", "mundo", "noite", "claro",
    "saber", "fazer", "poder", "certo", "feliz",
    "forte", "verde", "preto", "fundo", "baixo",
    "cheio", "vazio", "cinco", "prato", "ponto",
    "roupa", "vento", "tinta", "dente", "mente",
    "casar", "lutar", "jogar", "pular", "corpo",
    "rosto", "perna", "olhos", "nariz", "ombro",
    "chuva", "fogo", "calor", "festa", "tarde",
    "cinza", "prata", "areia", "linha", "papel",
    "ferro", "vidro", "chave", "cobre", "nobre",
    "justo", "mesmo", "velho", "jovem", "fraco"
]

def seed():
    db = SessionLocal()
    try:
        count = 0
        for p in PALAVRAS:
            p = p.upper()
            # verifica se a palavra ja existe no banco:
            existe = db.query(Palavra).filter(Palavra.palavra == p).first()
            if not existe:
                # se não existir, adiciona ao banco
                db.add(Palavra(palavra=p)) # db.add() não salva imediatamente, ele apenas marca o objeto para ser salvo. 
                count += 1
            db.commit() # o db.commit() é quem realmente envia tudo pro banco de uma vez no final
            print(f"{count} palavras inseridas")
    finally:
        db.close()

#  __name__ é uma variável especial que vale "__main__" 
# quando o arquivo é executado diretamente, e vale o nome 
# do módulo quando ele é importado por outro arquivo:

# python scripts/seed.py → __name__ é "__main__" → seed() é chamada
# from scripts.seed import seed em outro arquivo → __name__ é "scripts.seed" → seed() não é chamada automaticamente

if __name__ == "__main__":
    seed()