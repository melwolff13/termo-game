import pytest

from app.services.jogo import validar_tentativa, TentativaInvalida

def test_palavra_valida_passa(db):
    validar_tentativa("TERMO", db)

@pytest.mark.parametrize(
    "palavra",
    [
        "TERM",
        "TERMOS",
        "",
        "TE3MO",
        "TER-O",
        "TER O",
    ],
)
def test_formato_invalido(db, palavra):
    with pytest.raises(TentativaInvalida):
        validar_tentativa(palavra, db)


def test_palavra_fora_do_dicionario(db):
    with pytest.raises(TentativaInvalida):
        validar_tentativa("ZZZZZ", db)
