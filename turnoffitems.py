from app import db
from app.classes.item import Item_MarketItem
from app.classes.auth import Auth_User
from datetime import datetime, timedelta


# run every 12  hours
def main():
    """
    Go through the users and see if they havnt been online in 3 days
    :return:
    """
    threedays = datetime.utcnow() - (timedelta(days=3))
    users = db.session.query(Auth_User).filter(Auth_User.last_seen <= threedays, Auth_User.id != 1).all()
    for user in users:
        # put user on vacation
        user.vacation = 1
        # put there items on vacation
        markitem = db.session.query(Item_MarketItem).filter_by(vendor_id=user.id).all()
        for item in markitem:
            item.online = 0
            db.session.add(item)
            db.session.add(user)
    db.session.commit()


def putonline():
    # put everything online
    markitem = db.session.query(Item_MarketItem).filter_by(vendor_id=1).all()
    for item in markitem:
        item.online = 1
        db.session.add(item)
    db.session.commit()

main()
#putonline()