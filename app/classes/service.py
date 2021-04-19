from app import db


class shippingSecret(db.Model):
    __tablename__ = 'shippingSecret'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.INTEGER)
    timestamp = db.Column(db.DATETIME)
    txtmsg = db.Column(db.TEXT)
    orderid = db.Column(db.INTEGER)


class Returns(db.Model):
    __tablename__ = 'returns'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordernumber = db.Column(db.INTEGER)
    name = db.Column(db.Text)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    country = db.Column(db.Text)
    zip = db.Column(db.Text)
    message = db.Column(db.Text)


class DefaultReturns(db.Model):
    __tablename__ = 'defaultreturns'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    country = db.Column(db.Text)
    zip = db.Column(db.Text)
    message = db.Column(db.Text)
    username = db.Column(db.Text)
    userid = db.Column(db.INTEGER)


class ReturnsTracking(db.Model):
    __tablename__ = 'returntracking'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordernumber = db.Column(db.INTEGER)
    timestamp = db.Column(db.DATETIME)
    customername = db.Column(db.Text)
    customerid = db.Column(db.INTEGER)
    vendorname = db.Column(db.Text)
    vendorid = db.Column(db.INTEGER)
    carrier = db.Column(db.INTEGER)
    trackingnumber = db.Column(db.Text)
    othercarrier = db.Column(db.Text)


class Tracking(db.Model):
    __tablename__ = 'tracking'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.INTEGER)
    tracking1 = db.Column(db.Text)
    carrier1 = db.Column(db.Text)
    othercarrier1 = db.Column(db.Text)
    tracking2 = db.Column(db.Text)
    carrier2 = db.Column(db.Text)
    othercarrier2 = db.Column(db.Text)
    tracking3 = db.Column(db.Text)
    carrier3 = db.Column(db.Text)
    othercarrier3 = db.Column(db.Text)


class updateLog(db.Model):
    __tablename__ = 'updatelog'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header = db.Column(db.INTEGER)
    body = db.Column(db.INTEGER)
    dateofupdate = db.Column(db.TIMESTAMP())


class customerserviceitem(db.Model):
    __tablename__ = 'customerserviceonitem'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue = db.Column(db.Text)


class websitefeedback(db.Model):
    __tablename__ = 'websitefeedback'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    userid = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    comment = db.Column(db.Text)
    email = db.Column(db.Text)
    timestamp = db.Column(db.DATETIME)


class Issue(db.Model):
    __tablename__ = 'issues'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Text)
    author_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.DATETIME)
    admin = db.Column(db.INTEGER)
    status = db.Column(db.INTEGER)

db.create_all()
db.session.commit()