from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from smartsprout.models.store.usuario import Usuario

roles = ['Comum', 'Administrador', 'Estatístico', 'Operador']

class FormCriarConta(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar uma Conta')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()

        if usuario:
            raise ValidationError("Usuário já cadastrado. Cadastre com outro username, ou faça login para prosseguir")

class FormLogin(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField('Fazer Login')

class FormProduto(FlaskForm):
    nome_produto = StringField("Nome do produto", validators=[DataRequired(), Length(1, 10)])
    sensor_ultrassonico = StringField("Nome do sensor ultrassônico", validators=[DataRequired(), Length(1, 10)])
    sensor_umidade = StringField("Nome do sensor de umidade", validators=[DataRequired(), Length(1, 10)])
    rele = StringField("Nome do relê", validators=[DataRequired(), Length(1, 10)])
    bomba_agua = StringField("Nome da mini bomba d'água ", validators=[DataRequired(), Length(1, 10)])
    botao_submit_criarproduto = SubmitField("Criar um Produto")

class FormCriarUsuario(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    roles = SelectField("Selecionar Role", validators=[DataRequired()], choices=roles)
    botao_submit_criarusuario = SubmitField('Cadastrar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()

        if usuario:
            raise ValidationError("Usuário já cadastrado. Cadastre com outro username, ou faça login para prosseguir")

class FormEditarUsuario(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    botao_submit_editarusuario = SubmitField('Alterar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()

        if usuario:
            raise ValidationError("Usuário já cadastrado. Cadastre com outro username, ou faça login para prosseguir")