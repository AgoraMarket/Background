from app import db


class Categories(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'Agora_Market_Items'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.TEXT)


