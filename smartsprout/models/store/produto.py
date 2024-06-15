from smartsprout.models.db import db

#1 - 1: Um produto está associado a uma única venda ou troca
#(tipo, nula, a chave estrangeira da outra entidade (em letra minúscula))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(63), nullable=False)
    vendido = db.Column(db.Boolean, nullable=False, default=False)

    componentes = db.relationship('Componente', backref='produto', lazy=True)
    vendas = db.relationship('Venda', backref='produto', lazy=True)

