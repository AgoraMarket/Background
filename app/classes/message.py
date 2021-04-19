from app import db
from datetime import datetime


class Notifications(db.Model):
    __tablename__ = 'notifications'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.INTEGER)
    username = db.Column(db.TEXT)
    userid = db.Column(db.INTEGER)
    timestamp = db.Column(db.DateTime)
    salenumber = db.Column(db.INTEGER)
    bitcoin = db.Column(db.DECIMAL(20, 8))
    read = db.Column(db.INTEGER)


class Chat(db.Model):
    __tablename__ = 'chat'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderid = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    author = db.Column(db.Text)
    author_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.DATETIME)
    body = db.Column(db.Text)
    admin = db.Column(db.INTEGER)
    issueid = db.Column(db.INTEGER)


class Post(db.Model):
    __tablename__ = 'post'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())


class PostUser(db.Model):
    __tablename__ = 'postuser'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True)

    # type of message
    official = db.Column(db.Integer)
    dispute = db.Column(db.Integer)
    usermsg = db.Column(db.Integer)

    # info in msg
    body = db.Column(db.Text)
    subject = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer)

    itemid = db.Column(db.Integer)
    unread = db.Column(db.Integer)
    modid = db.Column(db.Integer)
    postid = db.Column(db.Integer)

    userid = db.Column(db.Integer)
    username = db.Column(db.Text)


class Comment(db.Model):
    __tablename__ = 'comment'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer)
    author = db.Column(db.Text)
    post_id = db.Column(db.Integer)
    modid = db.Column(db.Integer)



db.create_all()
db.session.commit()