from smartsprout.create_db import db

class Atuador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unidade = db.Column(db.String(4), nullable=False)
    topico = db.Column(db.String(20), nullable=False)
    id_componente = db.Column(db.Integer, db.ForeignKey('componente.id'), nullable=False)