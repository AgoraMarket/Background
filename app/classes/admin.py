from app import db

class AgoraFee(db.Model):
    __tablename__ = 'fees'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    itempurchase = db.Column(db.DECIMAL(20, 2))


class Agoraprofit_btc(db.Model):
    __tablename__ = 'account_profit_btc'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.DateTime, index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Agoraprofit_btccash(db.Model):
    __tablename__ = 'account_profit_btccash'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.DateTime, index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Agorafeeholdings(db.Model):
    __tablename__ = 'account_fee_holdings_btc'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.DateTime, index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Agorafeeholdings_btccash(db.Model):
    __tablename__ = 'account_fee_holdings_btc_cash'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.DateTime, index=True)
    total = db.Column(db.DECIMAL(20, 8))


class Agoraholdings(db.Model):
    __tablename__ = 'account_agoraholdings_btc'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.DateTime)
    userid = db.Column(db.INTEGER)
    total = db.Column(db.DECIMAL(20, 8))


class Agoraholdings_btccash(db.Model):
    __tablename__ = 'account_agoraholdings_btc_cash'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.DateTime)
    userid = db.Column(db.INTEGER)
    total = db.Column(db.DECIMAL(20, 8))


class Recaptcha(db.Model):
    __tablename__ = 'recaptcha'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    image = db.Column(db.INTEGER)
    answer = db.Column(db.Text)


class websiteOffline(db.Model):
    __tablename__ = 'websiteoffline'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    webstatus = db.Column(db.INTEGER)


class flagged(db.Model):
    __tablename__ = 'flagged'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    userid = db.Column(db.INTEGER)
    vendorname = db.Column(db.TEXT)
    howmany = db.Column(db.INTEGER)
    typeitem = db.Column(db.INTEGER)
    listingid= db.Column(db.INTEGER)
    listingtitle = db.Column(db.INTEGER)
    flaggeduserid1 = db.Column(db.INTEGER)
    flaggeduserid2 = db.Column(db.INTEGER)
    flaggeduserid3 = db.Column(db.INTEGER)
    flaggeduserid4 = db.Column(db.INTEGER)
    flaggeduserid5 = db.Column(db.INTEGER)


db.create_all()
db.session.commit()