from app.models.partida import Partida

def pegar_secreta(db, partida_id):
    game = db.query(Partida).filter(Partida.id == partida_id).first()
    return game.palavra_secreta.palavra