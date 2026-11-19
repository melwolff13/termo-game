from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.models.palavra import Palavra
from app.models.partida import Partida, StatusPartida
from app.models.tentativa import Tentativa

MAX_TENTATIVAS = 6

class PartidaNaoEncontrada(Exception):
    pass

def sortear_palavra(db: Session):
    palavra = (
        db.query(Palavra)
        .filter(Palavra.isAtivo == True)
        .order_by(func.random())
        .first()
    )
    if palavra is None:
        raise ValueError("Nenhuma palavra disponível no banco.")

    return palavra

def criar_partida(jogador_id: str, db: Session):
    palavra_secreta = sortear_palavra(db)
    nova_partida = Partida(
        jogador_id = jogador_id,
        palavra_secreta_id = palavra_secreta.id
    )
    db.add(nova_partida)
    db.commit()
    db.refresh(nova_partida)

    return {
        "partida_id": nova_partida.id,
        "jogador_id": nova_partida.jogador_id,
        "status": StatusPartida.EM_ANDAMENTO,
        "qtd_tentativas": 0,
        "tentativas_restantes": MAX_TENTATIVAS
    }

def comparar(tentativa: str, palavra_secreta: str):
    resultado = []

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

def validar_tentativa(tentativa: str, db: Session):
    if len(tentativa) != 5: 
        raise ValueError("A palavra deve conter 5 letras.")
    
    if not tentativa.isalpha():
        raise ValueError("A palavra deve conter apenas letras.")

    existe = (
        db.query(Palavra)
        .filter(Palavra.palavra == tentativa.upper())
        .first()
    )

    if not existe:
        raise ValueError("Palavra inválida.")

def controlar_jogada(partida_id: int, jogada: str, db: Session):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if partida is None:
        raise PartidaNaoEncontrada("Partida não encontrada.")

    if partida.status != StatusPartida.EM_ANDAMENTO:
        raise ValueError("Partida já encerrada.")

    jogada = jogada.strip().upper()
    validar_tentativa(jogada, db)

    resultado_tentativa = comparar(jogada, partida.palavra_secreta.palavra)

    tentativa = Tentativa(
        partida_id=partida.id,
        jogada=jogada,
        resultado=resultado_tentativa,
    )
    db.add(tentativa)
    partida.qtd_tentativas += 1

    if resultado_tentativa == ["verde"] * 5:
        partida.status = StatusPartida.VENCEU
        partida.finalizada_em = datetime.now(timezone.utc)
    elif partida.qtd_tentativas >= MAX_TENTATIVAS:
        partida.status = StatusPartida.PERDEU
        partida.finalizada_em = datetime.now(timezone.utc)

    db.commit()
    db.refresh(tentativa)

    return {
        "jogada": tentativa.jogada,
        "resultado": resultado_tentativa,
        "tentativas_usadas": partida.qtd_tentativas,
        "tentativas_restantes": MAX_TENTATIVAS - partida.qtd_tentativas,
        "status": partida.status,
        "palavra_secreta": (
            partida.palavra_secreta.palavra
            if partida.status != StatusPartida.EM_ANDAMENTO
            else None
        ),
    }

def consultar_partida(partida_id: int, db: Session):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if partida is None:
        raise PartidaNaoEncontrada("Partida não encontrada.")

    tentativas = (
        db.query(Tentativa)
        .filter(Tentativa.partida_id == partida.id)
        .order_by(Tentativa.id)
        .all()
    )

    return {
        "id": partida.id,
        "status": partida.status,
        "tentativas_usadas": partida.qtd_tentativas,
        "tentativas_restantes": MAX_TENTATIVAS - partida.qtd_tentativas,
        "tentativas": [
            {"jogada": t.jogada, "resultado": t.resultado}
            for t in tentativas
        ],
        "palavra_secreta": (
            partida.palavra_secreta.palavra if partida.status != StatusPartida.EM_ANDAMENTO else None
        ),
    }

def calcular_estatisticas(jogador_id: str, db: Session):
    # só partidas encerradas, da mais recente para a mais antiga
    partidas = (
        db.query(Partida)
        .filter(
            Partida.jogador_id == jogador_id,
            Partida.status != StatusPartida.EM_ANDAMENTO,
        )
        .order_by(Partida.id.desc())
        .all()
    )

    qtd_vitorias = sum(1 for p in partidas if p.status == StatusPartida.VENCEU)

    # sequência atual: vitórias seguidas a partir da mais recente
    sequencia_atual = 0
    for p in partidas:
        if p.status != StatusPartida.VENCEU:
            break
        sequencia_atual += 1

    # maior sequência: percorre tudo guardando o recorde
    maior_sequencia = 0
    contagem = 0
    for p in partidas:
        if p.status == StatusPartida.VENCEU:
            contagem += 1
            maior_sequencia = max(maior_sequencia, contagem)
        else:
            contagem = 0

    return {
        "qtd_partidas": len(partidas),
        "qtd_vitorias": qtd_vitorias,
        "sequencia_atual": sequencia_atual,
        "maior_sequencia": maior_sequencia,
    }