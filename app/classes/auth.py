# coding=utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db
from datetime import datetime


class UserFees(db.Model):
    __tablename__ = 'userfees'
    __bind_key__ = 'Agora_Market_Users'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    userid = db.Column(db.INTEGER)
    buyerfee = db.Column(db.DECIMAL(6, 4))
    buyerfee_time = db.Column(db.DATETIME)
    vendorfee = db.Column(db.DECIMAL(6, 4))
    vendorfee_time = db.Column(db.DATETIME)


class AccountSeedWords(db.Model):
    __tablename__ = 'AccountSeedWords'
    __bind_key__ = 'Agora_Market_Users'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    userid = db.Column(db.INTEGER)

    word00 = db.Column(db.String(30))
    word01 = db.Column(db.String(30))
    word02 = db.Column(db.String(30))
    word03 = db.Column(db.String(30))
    word04 = db.Column(db.String(30))
    word05 = db.Column(db.String(30))

    wordstring = db.column(db.text)



class User( db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'Agora_Market_Users'
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    username = db.Column(db.Text)
    password_hash = db.Column(db.Text)
    member_since = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    email = db.Column(db.Text)
    wallet_pin = db.Column(db.Text)
    profileimage = db.Column(db.Text)
    stringuserdir = db.Column(db.Text)
    bio = db.Column(db.TEXT)
    country = db.Column(db.Text)
    currency = db.Column(db.INTEGER)
    vendor_account = db.Column(db.INTEGER)
    selling_from = db.Column(db.Text)
    last_seen = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    admin = db.Column(db.INTEGER)
    admin_role = db.Column(db.INTEGER)
    dispute = db.Column(db.INTEGER)
    fails = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    vacation = db.Column(db.INTEGER)
    shopping_timer = db.Column(db.DATETIME)
    lasttraded_timer = db.Column(db.DATETIME)
    shard = db.Column(db.INTEGER)
    protosuser = db.Column(db.INTEGER)
    usernode = db.Column(db.INTEGER)
    affiliate_account = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    passwordpinallowed = db.Column(db.INTEGER)

    @staticmethod
    def cryptpassword(password):
        return generate_password_hash(password)

    @staticmethod
    def decryptpassword(pwdhash, password):
        return check_password_hash(pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)

        return s.dumps({'id': self.id}).decode('ascii')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)

        return True

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
