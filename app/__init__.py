from flask import Flask, request

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Ritchie'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/users.db'

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)

login.login_view = 'login'

from app import routes, models, errors