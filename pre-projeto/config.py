import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

# configurações
app = Flask(__name__)
app.app_context().push()
# aplicar o cross domein
CORS(app)
# caminho do banco de dados
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'project_flag.db')
# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

# segurança - JWT
app.config['JWT_SECRET_KEY'] = 'theAndrewislying'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes= 30)

jwt = JWTManager(app)

"""logging.basicConfig(
filename='meuslogs.log',
level=logging.INFO
)"""
