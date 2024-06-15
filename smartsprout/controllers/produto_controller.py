from flask import Blueprint, render_template, url_for, request
from smartsprout.forms import FormProduto
from smartsprout.models.store.produto import Produto
from smartsprout.models.iot.componente import Componente
from smartsprout.models.iot.sensor import Sensor
from smartsprout.models.iot.atuador import Atuador
from smartsprout.models.db import db


produto_ = Blueprint("produto", __name__, template_folder='templates')

@produto_.route("/produtos", methods=['GET', 'POST'])
def produtos():
    produtos = Produto.query.all()
    componentes = Componente.query.all()
    return render_template("produtos.html", produtos=produtos, componentes=componentes)

@produto_.route("/produto/forms_produto", methods=['GET', 'POST'])
def forms_produto():
    form_produto = FormProduto()

    def add_produto_componente_sensor(sensor_value, unidade, topico):
        sensor = Componente(
            nome = sensor_value,
            id_produto = produto.id
        )

        produto.componentes.append(sensor)
        db.session.add(produto)
        db.session.commit()

        sensor_s_ = Sensor(
            unidade = unidade,
            topico = topico,
            id_componente= sensor.id
        )

        sensor.sensores.append(sensor_s_)
        db.session.add(sensor)
        db.session.commit()

    def add_produto_componente_atuador(atuador_value, unidade, topico):
        atuador = Componente(
            nome = atuador_value,
            id_produto = produto.id
        )

        produto.componentes.append(atuador)
        db.session.add(produto)
        db.session.commit()

        atuador_at_ = Atuador(
            unidade = unidade,
            topico = topico,
            id_componente= atuador.id
        )

        atuador.atuadores.append(atuador_at_)
        db.session.add(atuador)
        db.session.commit()

    if form_produto.validate_on_submit():
        #Novo produto
        produto = Produto(nome=form_produto.nome_produto.data)

        #novo sensor ultrassônico
        add_produto_componente_sensor(form_produto.sensor_ultrassonico.data, "cm", "/irrigacao/enviar")
        add_produto_componente_sensor(form_produto.sensor_umidade.data, "%", "/irrigacao/enviar")
        add_produto_componente_atuador(form_produto.rele.data, "V", "irrigacao/receber")
        add_produto_componente_atuador(form_produto.bomba_agua.data, "gpm", "irrigacao/receber")

        produtos = Produto.query.all()
        componentes = Componente.query.all()

        return render_template("produtos.html",  produtos=produtos, componentes=componentes)

    return render_template("forms_produto.html", form_produto=form_produto)


@produto_.route("/deletar_produto/<id_produto>", methods=['GET', 'POST'])
def deletar_produto(id_produto):
    produto = Produto.query.get(id_produto)
    ids_sensores = []
    ids_atuadores = []

    if produto.vendido == False:

        componentes = Componente.query.filter_by(id_produto=produto.id)

        for componente in componentes:
            ids_sensores.append(componente.id)
            ids_atuadores.append(componente.id)

        sensores = Sensor.query.filter(Sensor.id_componente.in_(ids_sensores))
        atuadores = Atuador.query.filter(Atuador.id_componente.in_(ids_atuadores))


        for sensor in sensores:
            db.session.delete(sensor)

        for atuador in atuadores:
            db.session.delete(atuador)

        for componente in componentes:
            db.session.delete(componente)

        db.session.delete(produto)
        db.session.commit()

        produtos = Produto.query.all()
        componentes = Componente.query.all()

        return render_template("produtos.html", produtos=produtos, componentes=componentes)

    produtos = Produto.query.all()
    componentes = Componente.query.all()

    return render_template("produtos.html", produtos=produtos, componentes=componentes)


@produto_.route("editar_produto/<id_produto>", methods=['GET', 'POST'])
def editar_produto(id_produto):
    produto = Produto.query.get(id_produto)
    componentes_forms = Componente.query.filter_by(id_produto=id_produto).all()

    form_produto = FormProduto()

    if request.method == "GET":
        form_produto.nome_produto.data = produto.nome
        form_produto.sensor_ultrassonico.data = componentes_forms[0].nome
        form_produto.sensor_umidade.data = componentes_forms[1].nome
        form_produto.rele.data = componentes_forms[2].nome
        form_produto.bomba_agua.data = componentes_forms[3].nome

    elif form_produto.validate_on_submit() and 'botao_submit_criarproduto' in request.form:
        produto.nome = form_produto.nome_produto.data
        componentes_forms[0].nome = form_produto.sensor_ultrassonico.data
        componentes_forms[1].nome = form_produto.sensor_umidade.data
        componentes_forms[2].nome = form_produto.rele.data
        componentes_forms[3].nome = form_produto.bomba_agua.data

        db.session.commit()

        produtos = Produto.query.all()
        componentes = Componente.query.all()

        return render_template("produtos.html", produtos=produtos, componentes=componentes)

    return render_template("editar_produto.html", id_produto=id_produto, produto=produto, form_produto=form_produto)
