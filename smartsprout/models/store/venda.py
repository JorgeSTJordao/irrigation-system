from smartsprout.models.db import db

#N - 1: Várias vendas associadas um objeto
#(tipo, nula, a chave estrangeira da outra entidade (em letra minúscula))

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
