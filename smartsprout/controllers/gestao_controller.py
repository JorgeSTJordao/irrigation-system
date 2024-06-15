from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required

from smartsprout.models.db import db
from smartsprout.models.store.usuario import Usuario
from smartsprout.models.store.produto import Produto
from smartsprout.models.iot.componente import Componente
from smartsprout.models.store.venda import Venda
from smartsprout.forms import FormCriarUsuario, FormEditarUsuario
from smartsprout import bcrypt

gestao_ = Blueprint("gestao", __name__, template_folder='templates')

@gestao_.route("/gestao", methods=['GET', 'POST'])
@login_required
def gestao():
    usuario = None
    form_criarusuario = FormCriarUsuario()
    form_editarusuario = FormEditarUsuario()

    if form_criarusuario.validate_on_submit() and 'botao_submit_criarusuario' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarusuario.senha.data)

        usuario = Usuario(
            username=form_criarusuario.username.data,
            senha=senha_crypt,
            roles=form_criarusuario.roles.data.lower()
        )

        db.session.add(usuario)
        db.session.commit()

    usuarios = Usuario.query.all()

    return render_template(
        "gestao.html",
        usuario=usuario,
        form_editarusuario=form_editarusuario,
        form_criarusuario=form_criarusuario,
        usuarios=usuarios)

@gestao_.route("/gestao/<id_usuario>", methods=['GET', 'POST'])
def gestao_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    vendas = Venda.query.filter_by(id_usuario=id_usuario).all()

    usuarios_produtos = (db.session.query(Usuario, Venda, Produto, Componente)
                         .filter(Venda.id_usuario == id_usuario)
                         .join(Venda, Usuario.id == Venda.id_usuario)
                         .join(Produto, Venda.id_produto == Produto.id)
                         .join(Componente, Produto.id == Componente.id_produto)
                         .all())

    produtos_filtrados = {}

    for usuario, venda, produto, componente in usuarios_produtos:
        if produto not in produtos_filtrados:
            produtos_filtrados[produto] = []
        produtos_filtrados[produto].append(componente)


    form_criarusuario = FormCriarUsuario()
    form_editarusuario = FormEditarUsuario()

    if form_criarusuario.validate_on_submit():
        senha_crypt = bcrypt.generate_password_hash(form_criarusuario.senha.data)

        usuario = Usuario(
            username=form_criarusuario.username.data,
            senha=senha_crypt,
            roles=form_criarusuario.roles.data.lower()
        )

        db.session.add(usuario)
        db.session.commit()

    if form_editarusuario.validate_on_submit():
        usuario.username = form_editarusuario.username.data
        db.session.commit()

    usuarios = Usuario.query.all()

    return render_template(
        "gestao.html",
        usuario=usuario,
        usuarios=usuarios,
        produtos_filtrados=produtos_filtrados,
        usuarios_produtos=usuarios_produtos,
        form_criarusuario=form_criarusuario,
        form_editarusuario=form_editarusuario)


@gestao_.route("/gestao/venda/<id_usuario>", methods=['GET', 'POST'])
def gestao_venda(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    produtos = Produto.query.filter_by(vendido=False).all()
    componentes = Componente.query.all()

    return render_template("vendas.html", id_usuario=id_usuario, usuario=usuario, produtos=produtos, componentes=componentes)

@gestao_.route("/gestao/venda/<id_usuario>/<id_produto>", methods=['GET', 'POST'])
def gestao_vendido(id_usuario, id_produto):
    venda = Venda(id_usuario=id_usuario, id_produto=id_produto)
    usuario = Usuario.query.get(id_usuario)
    produto = Produto.query.get(id_produto)

    usuario.vendas.append(venda)
    produto.vendas.append(venda)
    db.session.add(venda)
    db.session.commit()

    produto.vendido = True
    db.session.commit()

    produtos = Produto.query.filter_by(vendido=False).all()
    componentes = Componente.query.all()

    return render_template("vendas.html", id_usuario=id_usuario, usuario=usuario, produtos=produtos, componentes=componentes)

@gestao_.route("/gestao/<id_usuario>/excluir", methods=['GET', 'POST'])
def gestao_deletar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    vendas = Venda.query.filter_by(id_usuario=id_usuario).first()

    if vendas == None:
        db.session.delete(usuario)
        db.session.commit()

    return redirect("/gestao")

