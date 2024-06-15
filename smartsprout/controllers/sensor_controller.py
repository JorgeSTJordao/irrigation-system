import json
from smartsprout.models.db import db
from flask import Blueprint, render_template, request, current_app
from smartsprout.models.store.usuario import Usuario
from smartsprout.models.store.produto import Produto
from smartsprout.models.store.venda import Venda
from smartsprout.models.iot.componente import Componente
from smartsprout.models.iot.sensor import Sensor
from smartsprout.models.iot.leitura import Leitura
from datetime import datetime
from smartsprout.mqtt_connection import mqtt_client, topic_subscribe

sensor_ = Blueprint("sensor", __name__, template_folder='templates')
sensores_valores = []

def usuarios_filtrados_fun():
    usuarios_produtos = (db.session.query(Usuario, Venda, Produto)
                         .join(Venda, Usuario.id == Venda.id_usuario)
                         .join(Produto, Venda.id_produto == Produto.id)
                         .order_by(Usuario.username))

    usuarios_filtrados = {}

    for usuario, venda, produto in usuarios_produtos:
        if venda.id not in usuarios_filtrados:
            usuarios_filtrados[venda] = []
            usuarios_filtrados[venda].append(usuario)
            usuarios_filtrados[venda].append(produto)

    return usuarios_filtrados


@sensor_.route("/sensores", methods=['POST', 'GET'])
def sensores():
    venda = None
    usuarios_filtrados = usuarios_filtrados_fun()

    return render_template("sensores.html", venda=venda, usuarios_filtrados=usuarios_filtrados)


@sensor_.route("/sensores/sensor_especifico", methods=["POST", "GET"])
def sensores_venda():

    id_venda = request.form.get('select_user')
    usuarios_filtrados = usuarios_filtrados_fun()


    componentes = (db.session.query(Usuario, Venda, Produto, Componente, Sensor)
                         .filter(Venda.id == id_venda)
                         .join(Venda, Usuario.id == Venda.id_usuario)
                         .join(Produto, Venda.id_produto == Produto.id)
                         .join(Componente, Produto.id == Componente.id_produto)
                        .join(Sensor, Sensor.id_componente == Componente.id)
                         .all())

    sensores_valores.append(componentes[0][3])
    sensores_valores.append(componentes[1][3])

    return render_template(
        "sensores.html",
        sensores_valores=sensores_valores,
        usuarios_filtrados=usuarios_filtrados)