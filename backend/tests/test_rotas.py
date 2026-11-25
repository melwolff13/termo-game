import pytest

from app.models.partida import StatusPartida
from app.models.palavra import Palavra
from tests.helpers import pegar_secreta

PALAVRAS = ["TERMO", "PENSO", "ARARA"]
JOGADOR = {"jogador_id": "jogador-teste"}


def criar(client):
    resp = client.post("/partidas/", json=JOGADOR)
    assert resp.status_code == 201
    return resp.json()["partida_id"]


def tentar(client, partida_id, jogada):
    return client.post(f"/partidas/{partida_id}/tentativa", json={"jogada": jogada})


def test_criar_partida_retorna_estado_inicial(client, db):
    resp = client.post("/partidas/", json=JOGADOR)

    assert resp.status_code == 201
    dados = resp.json()
    assert dados["status"] == StatusPartida.EM_ANDAMENTO.value
    assert dados["qtd_tentativas"] == 0
    assert dados["tentativas_restantes"] == 6
    assert pegar_secreta(db, dados["partida_id"]) not in resp.text


def test_criar_partida_sem_palavras_retorna_422(client, db):
    db.query(Palavra).delete()
    db.commit()

    resp = client.post("/partidas/", json=JOGADOR)

    assert resp.status_code == 422


def test_secreta_nao_aparece_durante_a_partida(client, db):
    partida_id = criar(client)
    secreta = pegar_secreta(db, partida_id)
    errada = next(p for p in PALAVRAS if p != secreta)

    resp_tentativa = tentar(client, partida_id, errada)
    resp_estado = client.get(f"/partidas/{partida_id}")

    assert resp_tentativa.json()["palavra_secreta"] is None
    assert resp_estado.json()["palavra_secreta"] is None
    assert secreta not in resp_tentativa.text
    assert secreta not in resp_estado.text


def test_tentativa_valida_e_registrada(client, db):
    partida_id = criar(client)
    secreta = pegar_secreta(db, partida_id)
    errada = next(p for p in PALAVRAS if p != secreta)

    resp = tentar(client, partida_id, errada)

    assert resp.status_code == 200
    assert resp.json()["tentativas_usadas"] == 1
    assert resp.json()["tentativas_restantes"] == 5

    estado = client.get(f"/partidas/{partida_id}").json()
    assert len(estado["tentativas"]) == 1
    assert estado["tentativas"][0]["jogada"] == errada


def test_jogada_em_minusculas_e_normalizada(client, db):
    partida_id = criar(client)
    secreta = pegar_secreta(db, partida_id)
    errada = next(p for p in PALAVRAS if p != secreta)

    resp = tentar(client, partida_id, errada.lower())

    assert resp.status_code == 200
    assert resp.json()["jogada"] == errada


@pytest.mark.parametrize("jogada", ["ZZZZZ", "TERM", "TERMOS", "TE3MO"])
def test_palavra_invalida_nao_gasta_tentativa(client, jogada):
    partida_id = criar(client)

    resp = tentar(client, partida_id, jogada)

    assert resp.status_code == 422
    estado = client.get(f"/partidas/{partida_id}").json()
    assert estado["tentativas_usadas"] == 0


def test_fluxo_de_vitoria(client, db):
    partida_id = criar(client)
    secreta = pegar_secreta(db, partida_id)

    resp = tentar(client, partida_id, secreta)

    assert resp.status_code == 200
    assert resp.json()["resultado"] == ["verde"] * 5

    estado = client.get(f"/partidas/{partida_id}").json()
    assert estado["status"] == StatusPartida.VENCEU.value
    assert estado["palavra_secreta"] == secreta


def test_fluxo_de_derrota(client, db):
    partida_id = criar(client)
    secreta = pegar_secreta(db, partida_id)
    errada = next(p for p in PALAVRAS if p != secreta)

    for _ in range(6):
        assert tentar(client, partida_id, errada).status_code == 200

    estado = client.get(f"/partidas/{partida_id}").json()
    assert estado["status"] == StatusPartida.PERDEU.value
    assert estado["tentativas_restantes"] == 0
    assert estado["palavra_secreta"] == secreta


def test_partida_encerrada_retorna_409(client, db):
    partida_id = criar(client)
    secreta = pegar_secreta(db, partida_id)
    tentar(client, partida_id, secreta)   # vence

    resp = tentar(client, partida_id, secreta)

    assert resp.status_code == 409


def test_partida_inexistente_retorna_404(client):
    assert client.get("/partidas/9999").status_code == 404
    assert tentar(client, 9999, "TERMO").status_code == 404


def test_rota_de_estatisticas(client, db):
    resp = client.get("/stats/jogador-sem-partidas")

    assert resp.status_code == 200
    assert resp.json()["qtd_partidas"] == 0