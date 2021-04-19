from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI,\
    SQLALCHEMY_BINDS,\
    customlog,\
    SHARDBTCCASH,\
    SHARD
from flask_mail import Mail
from datetime import datetime


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
app.config['SHARD'] = SHARD
app.config['SHARDBTCCASH'] = SHARDBTCCASH


db = SQLAlchemy(app)
mail = Mail(app)


def errorLogger(function, error, kindoferror, user):
    now = str(datetime.utcnow())
    #1= other
    #2 = database
    #3 = bitcoin
    #4 = bitcoin
    u = str(user)
    if kindoferror == 1:
        with open (customlog + "Error-errorlog.txt", "a") as text_file:
            text_file.write(now + '-' + str(function) + '-' + u + '-' + str(error) + '\n')
    if kindoferror ==2:
        with open(customlog + "Database-errorlog.txt", "a") as text_file:
            text_file.write(now + '-' + str(function) + '-' + u + '-' + str(error) + '\n')

    if kindoferror == 3:
        with open(customlog + "Bitcoin-errorlog.txt", "a") as text_file:
            text_file.write(now + '-' + str(function) + '-' + u + '-' + str(error) + '\n')

    if kindoferror == 4:
        with open(customlog + "Wallet-errorlog.txt", "a") as text_file:
            text_file.write(now + '-' + str(function) + '-' + u + '-'+ str(error) + '\n')
