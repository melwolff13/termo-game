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
    'forca', 'prova', 'saber', 'fazer', 'cinco', 'prato', 'vento', 'perna', 'olhos', 'zelar', 
    'cinza', 'mesmo', 'velho', 'fraco', 'abrir', 'achar', 'acima', 'adiar', 'afeto', 'agora', 
    'ajuda', 'amigo', 'andar', 'anexo', 'antes', 'apoio', 'areia', 'armar', 'aroma', 'assar', 
    'astro', 'ativo', 'atuar', 'audaz', 'aviso', 'azedo', 'baixo', 'baile', 'banco', 'barco', 
    'barra', 'beijo', 'bicho', 'blusa', 'bolsa', 'borda', 'brasa', 'bravo', 'brejo', 'brisa', 
    'broto', 'cabra', 'cacho', 'caixa', 'caldo', 'calma', 'calor', 'campo', 'canal', 'canto', 
    'capaz', 'carga', 'carne', 'carro', 'carta', 'casal', 'casar', 'casca', 'ceder', 'censo', 
    'cerca', 'certo', 'chave', 'cheio', 'chuva', 'claro', 'cobre', 'coisa', 'colar', 'comer', 
    'conta', 'coral', 'corpo', 'corte', 'costa', 'couro', 'criar', 'crise', 'culpa', 'curar', 
    'curso', 'dardo', 'dente', 'dizer', 'dogma', 'dorso', 'duelo', 'durar', 'elite', 'errar', 
    'falar', 'falha', 'fardo', 'farta', 'festa', 'feixe', 'feliz', 'feroz', 'ferro', 'fibra', 
    'ficar', 'final', 'firma', 'fitar', 'fluir', 'focar', 'folha', 'fonte', 'forma', 'forte', 
    'fraco', 'frase', 'freio', 'fruta', 'fugir', 'fundo', 'ganho', 'garra', 'gasto', 'gelar', 
    'gerar', 'girar', 'golpe', 'gosto', 'grato', 'grito', 'grupo', 'guiar', 'honra', 'hotel', 
    'idade', 'igual', 'impar', 'jogar', 'jovem', 'junto', 'justo', 'largo', 'laser', 'lazer', 
    'leite', 'lenda', 'lento', 'limpo', 'linha', 'livro', 'local', 'louro', 'lugar', 'lutar', 
    'magia', 'maior', 'manso', 'marca', 'matar', 'medir', 'menor', 'mente', 'metal', 'metro', 
    'misto', 'moeda', 'morar', 'morro', 'mover', 'mundo', 'mural', 'museu', 'nadar', 'nariz', 
    'natal', 'navio', 'negar', 'nervo', 'nobre', 'noite', 'norte', 'nuvem', 'obter', 'ombro', 
    'ordem', 'ouvir', 'pacto', 'padre', 'pagar', 'palco', 'papel', 'parar', 'parte', 'passo', 
    'pasta', 'pedra', 'pegar', 'peito', 'perto', 'pesca', 'piano', 'pilha', 'pingo', 'pista', 
    'plano', 'poder', 'ponto', 'porta', 'praia', 'prata', 'prazo', 'preto', 'prova', 'pular', 
    'queda', 'quilo', 'raiva', 'reino', 'repor', 'rezar', 'risco', 'ritmo', 'rocha', 'rosto', 
    'roupa', 'saber', 'sabor', 'sacar', 'salto', 'selva', 'senso', 'serra', 'servo', 'sinal', 
    'sobra', 'sogra', 'sonho', 'sopro', 'sorte', 'suave', 'subir', 'surto', 'talha', 'tarde', 
    'tecer', 'tempo', 'tenro', 'terra', 'tinta', 'tirar', 'tocar', 'torre', 'trama', 'trapo', 
    'trevo', 'troca', 'turma', 'urgir', 'valer', 'valor', 'vazio', 'verde', 'verbo', 'verme', 
    'verso', 'veste', 'vidro', 'vigia', 'vigor', 'vinho', 'virar', 'vista', 'viver', 'vulto', 
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