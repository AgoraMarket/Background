from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI,\
    SQLALCHEMY_BINDS,\
    SHARDBTCCASH
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
app.config['SHARDBTCCASH'] = SHARDBTCCASH


db = SQLAlchemy(app)
mail = Mail(app)
UPLOADED_FILES_DEST = '/nfs'
