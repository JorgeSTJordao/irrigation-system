from flask import Blueprint, render_template, request, flash
from smartsprout.forms import FormLogin, FormCriarConta
from smartsprout.models.db import db
from smartsprout.models.store.usuario import Usuario
from flask_login import login_user, logout_user
from smartsprout import bcrypt


app_ = Blueprint("app", __name__, template_folder='templates')

@app_.route("/", methods=["GET", "POST"])

def index():
    return render_template("index.html")

@app_.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(username=form_login.username.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            flash(f"Login feito com sucesso com o usuário {form_login.username.data}")
            return render_template("home.html")
        else:
            flash(f"Falha no login. Usuário ou senha incorretos")

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(
            username=form_criarconta.username.data,
            senha=senha_crypt
        )

        db.session.add(usuario)
        db.session.commit()

        flash(f"Conta criada com o usuário {form_criarconta.username.data}")
        return render_template("home.html")

    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta)

@app_.route("/home")
def home():
    return render_template("home.html")

@app_.route("/sair")
def sair():
    logout_user()
    return render_template("home.html")

