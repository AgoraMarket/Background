from app import db


class userHistory(db.Model):
    __tablename__ = 'userhistory'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.INTEGER)
    recentcat1 = db.Column(db.INTEGER)
    recentcat1date = db.Column(db.DATETIME)
    recentcat2 = db.Column(db.INTEGER)
    recentcat2date = db.Column(db.DATETIME)
    recentcat3 = db.Column(db.INTEGER)
    recentcat3date = db.Column(db.DATETIME)
    recentcat4 = db.Column(db.INTEGER)
    recentcat4date = db.Column(db.DATETIME)
    recentcat5 = db.Column(db.INTEGER)
    recentcat5date = db.Column(db.DATETIME)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    __bind_key__ = 'Agora_Market'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customername = db.Column(db.Text)
    sale_id = db.Column(db.INTEGER)
    vendorname = db.Column(db.Text)
    vendorid = db.Column(db.INTEGER)
    comment = db.Column(db.Text)
    itemrating = db.Column(db.INTEGER)
    item_id = db.Column(db.Integer)
    type = db.Column(db.INTEGER)
    vendorrating = db.Column(db.INTEGER)
    timestamp = db.Column(db.DateTime)
    addedtodb = db.Column(db.INTEGER)
    author_id = db.Column(db.Integer)



db.create_all()
db.session.commit()