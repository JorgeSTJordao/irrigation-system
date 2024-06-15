from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

app = Flask(__name__, root_path="./", template_folder='smartsprout/templates')

app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'key-generated'

#Local onde será criado o banco de dados
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from smartsprout.models.db import db, instance
from smartsprout.models.store.usuario import Usuario
from smartsprout.models.store.venda import Venda
from smartsprout.models.store.produto import Produto
from smartsprout.models.iot.componente import Componente
from smartsprout.models.iot.leitura import Leitura


app.config['SQLALCHEMY_DATABASE_URI'] = instance

db.init_app(app)

from smartsprout.controllers.app_controller import app_
from smartsprout.controllers.produto_controller import produto_
from smartsprout.controllers.sensor_controller import sensor_
from smartsprout.controllers.atuador_controller import atuador_
from smartsprout.controllers.gestao_controller import gestao_
from smartsprout.models.iot.leitura import Leitura
from smartsprout.models.iot.escrita import Escrita

app.register_blueprint(app_, url_prefix='/')
app.register_blueprint(produto_, url_prefix='/')
app.register_blueprint(sensor_, url_prefix='/')
app.register_blueprint(atuador_, url_prefix='/')
app.register_blueprint(gestao_, url_prefix='/')


