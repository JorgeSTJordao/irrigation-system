from smartsprout.create_db import db
from smartsprout.models.iot.sensor import Sensor
from datetime import datetime

class Leitura(db.Model):
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    leitura_datetime = db.Column(db.DateTime(), nullable=False)
    valor = db.Column(db.Float, nullable=True)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)



