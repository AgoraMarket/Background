from app import db


class PromotedItem(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'Agora_Market_Items_promoted'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    itemid = db.Column(db.INTEGER)

