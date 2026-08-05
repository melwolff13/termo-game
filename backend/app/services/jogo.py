from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import SessionLocal
from app.models.palavra import Palavra

def sortear_palavra(db: Session):
    palavra = (
        db.query(Palavra)
        .filter(Palavra.isAtivo == True)
        .order_by(func.random())
        .first()
    )

    return palavra

def comparar(tentativa: str, palavra_secreta:str):
    resultado = []
    tentativa = tentativa.upper()

    contador = {}
    for letra in palavra_secreta:
        if letra not in contador:
            contador[letra] = 1
        else:
            contador[letra] += 1
    # print("1a contagem:", contador)

    for i, letra in enumerate(tentativa):
        if letra == palavra_secreta[i] and contador[letra] > 0:
            resultado.append("verde")
            contador[letra] -= 1
        else:
            resultado.append("cinza")
    # print("2a contagem:", contador)

    for i, letra in enumerate(tentativa):
        if letra in palavra_secreta and contador[letra] > 0 and resultado[i] != "verde":
            resultado[i] = "amarelo"
            contador[letra] -= 1
    # print("3a contagem:", contador)

    return(resultado)






if __name__ == "__main__":
    db = SessionLocal()
    try:
        resultado = sortear_palavra(db)
        palavra = resultado.palavra

        for i in range(5):
            tentativa = input("tentativa: ")
            jogada = comparar(tentativa, palavra)
            if jogada == ["verde"]*5:
                print("ebaa, acertou!")
                break
            else:
                print(jogada)
        print(f"a palavra era {palavra}")
    finally:
        db.close()