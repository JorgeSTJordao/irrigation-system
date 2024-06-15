from smartsprout import db, login_manager
from flask_login import UserMixin

#1 - N: essa relação é criada dentro da tabela que pode ter vários objetos
#(nome da tabela (class.py), nome de referência para outra entidade, lazy=retorna todos os dados)

#função que encontra o usuário durante alguma operação de entrada
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    roles = db.Column(db.String(20), nullable=False, default='comum')
    vendas = db.relationship('Venda', backref='consumidor', lazy=True)
