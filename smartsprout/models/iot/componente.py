from smartsprout.create_db import db

class Componente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    ligado = db.Column(db.Boolean, nullable=False, default=False)



    #chaves estrangeiras
    sensores = db.relationship('Sensor', backref='componente_sensor', lazy=True)
    atuadores = db.relationship('Atuador', backref='componente_atuador', lazy=True)

