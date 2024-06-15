from smartsprout.create_db import db


class Escrita(db.Model):
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    escrita_datetime = db.Column(db.DateTime(), nullable=False)
    valor = db.Column(db.Float, nullable=True)
    atuador_id = db.Column(db.Integer, db.ForeignKey('atuador.id'), nullable=False)
