import pytest

from app.services.jogo import comparar

V, A, C = "verde", "amarelo", "cinza"

def test_comparar_sem_letras_repetidas():
    resultado = comparar(tentativa="PENSO", palavra_secreta="TENTO")
    assert resultado == [C, V, V, C, V]

@pytest.mark.parametrize(
    "secreta, tentativa, esperado",
    [
        ("TERMO", "TERMO", [V, V, V, V, V]), # acerto total
        ("TERMO", "TERRA", [V, V, V, C, C]), # 2º R cinza
        ("TERMO", "ERROR", [A, C, V, A, C]), # R da pos. 2 não rouba o verde da pos. 3
        ("CARRO", "ARARA", [A, A, C, V, C]), # vários A
        ("CARRO", "RATOS", [A, V, C, A, C]), # secreta repetida, tentativa não
    ],
)
def test_comparar_com_letras_repetida(secreta, tentativa, esperado):
    assert comparar(tentativa=tentativa, palavra_secreta=secreta) == esperado