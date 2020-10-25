from random import random
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from sqlalchemy import asc, desc, or_

app = Flask(__name__)
app.debug = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'Ritchie2020-06-16'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # add on 2020-06-14
app.config["CLIENT_IMAGES"] = "/Users/Ritchie/Documents/financial-computing-app/app/static/images"
app.config["CLIENT_REPORTS"] = "/Users/Ritchie/Documents/financial-computing-app/app/static/client/reports"
app.config["CLIENT_CSV"] = "/Users/Ritchie/Documents/financial-computing-app/app/static/download/"
app.config["APP_DIRECTORY"] = "/Users/Ritchie/Documents/financial-computing-app/app/"
# Send emails 
# app.config['DEBUG'] = True
# app.config['MAIL_SERVER'] ='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'brian.liu1618@gmail.com' # 如果验证失败，需要在google account里进行第三方登录允许设置
# app.config['MAIL_PASSWORD'] = 'chaplin525'
# app.config['MAIL_DEFAULT_SENDER'] = 'brian.liu1618@gmail.com'
# app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_ASCII_ATTACHMENTS'] = False
#mail = Mail()
#mail.init_app(app)
# put following 4 lines in applications def
# def send_email():
#     mail = Mail(app) 放在应用里才行
#     msg = Message('Hello', sender = 'brian.liu1618@gmail.com', recipients = ['brian.liu1618@gmail.com'])
#     msg.body = "Hello Flask message sent from Flask-Mail"
#     mail.send(msg)
# ------

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)

login.login_view = 'login'

from app import routes, models, errors