from app.models.partida import Partida, StatusPartida
from app.services.jogo import calcular_estatisticas


def _partida(db, palavra_id, status, jogador="j1"):
    p = Partida(jogador_id=jogador, palavra_secreta_id=palavra_id, status=status)
    db.add(p)
    db.commit()


def test_estatisticas_sequencias(db):
    # ordem de criação: V V D V V V  → atual = 3, maior = 3
    for s in [StatusPartida.VENCEU, StatusPartida.VENCEU, StatusPartida.PERDEU, StatusPartida.VENCEU, StatusPartida.VENCEU, StatusPartida.VENCEU]:
        _partida(db, 1, s)

    r = calcular_estatisticas("j1", db)

    assert r == {"qtd_partidas": 6, "qtd_vitorias": 5, "sequencia_atual": 3, "maior_sequencia": 3}


def test_sequencia_atual_zera_apos_derrota(db):
    for s in [StatusPartida.VENCEU, StatusPartida.VENCEU, StatusPartida.PERDEU]:
        _partida(db, 1, s)

    r = calcular_estatisticas("j1", db)

    assert r["sequencia_atual"] == 0
    assert r["maior_sequencia"] == 2


def test_partida_em_andamento_nao_conta(db):
    _partida(db, 1, StatusPartida.VENCEU)
    _partida(db, 1, StatusPartida.EM_ANDAMENTO)

    assert calcular_estatisticas("j1", db)["qtd_partidas"] == 1


def test_estatisticas_sao_por_jogador(db):
    _partida(db, 1, StatusPartida.VENCEU, jogador="j1")
    _partida(db, 1, StatusPartida.VENCEU, jogador="j2")

    assert calcular_estatisticas("j1", db)["qtd_partidas"] == 1
