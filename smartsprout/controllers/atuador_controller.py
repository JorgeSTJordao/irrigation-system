from smartsprout.models.db import db
from flask import Blueprint, render_template, request
from smartsprout.models.store.usuario import Usuario
from smartsprout.models.store.produto import Produto
from smartsprout.models.store.venda import Venda
from smartsprout.models.iot.componente import Componente
from smartsprout.models.iot.atuador import Atuador

atuador_ = Blueprint("atuador", __name__, template_folder='templates')
atuadores_valores = []

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

@atuador_.route("/configuracoes")
def configuracoes():
    venda = None
    usuarios_filtrados = usuarios_filtrados_fun()

    return render_template("configuracoes.html", venda=venda, usuarios_filtrados=usuarios_filtrados)

@atuador_.route("/configuracoes/atuador_especifico", methods=["POST", "GET"])
def configuracoes_venda():

    id_venda = request.form.get('select_user')
    usuarios_filtrados = usuarios_filtrados_fun()


    componentes = (db.session.query(Usuario, Venda, Produto, Componente, Atuador)
                         .filter(Venda.id == id_venda)
                         .join(Venda, Usuario.id == Venda.id_usuario)
                         .join(Produto, Venda.id_produto == Produto.id)
                         .join(Componente, Produto.id == Componente.id_produto)
                        .join(Atuador, Atuador.id_componente == Componente.id)
                         .all())

    atuadores_valores.append(componentes[0][3])
    atuadores_valores.append(componentes[1][3])

    return render_template(
        "configuracoes.html",
        atuadores_valores=atuadores_valores,
        usuarios_filtrados=usuarios_filtrados)
