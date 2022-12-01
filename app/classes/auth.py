
from flask_login import UserMixin, AnonymousUserMixin
from app import db, ma, login_manager
from datetime import datetime
from uuid import uuid4


def get_uuid():
    return uuid4().hex


class Auth_UserFees(db.Model):
    __tablename__ = 'auth_user_fees'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    buyerfee = db.Column(db.DECIMAL(6, 4))
    buyerfee_time = db.Column(db.TIMESTAMP())
    vendorfee = db.Column(db.DECIMAL(6, 4))
    vendorfee_time = db.Column(db.TIMESTAMP())


class Auth_UserFees_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Auth_UserFees
    id = ma.auto_field()
    user_id = ma.auto_field()
    buyerfee = ma.auto_field()
    buyerfee_time = ma.auto_field()
    vendorfee = ma.auto_field()
    vendorfee_time = ma.auto_field()


class Auth_AccountSeedWords(db.Model):
    __tablename__ = 'auth_account_seed_words'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    word00 = db.Column(db.VARCHAR(30))
    word01 = db.Column(db.VARCHAR(30))
    word02 = db.Column(db.VARCHAR(30))
    word03 = db.Column(db.VARCHAR(30))
    word04 = db.Column(db.VARCHAR(30))
    word05 = db.Column(db.VARCHAR(30))
    wordstring = db.Column(db.TEXT)


class Auth_AccountSeedWords_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Auth_AccountSeedWords

    user_id = ma.auto_field()
    word00 = ma.auto_field()
    word01 = ma.auto_field()
    word02 = ma.auto_field()
    word03 = ma.auto_field()
    word04 = ma.auto_field()
    word05 = ma.auto_field()
