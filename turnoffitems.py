from app import db
from app.classes.item import marketItem
from app.classes.auth import User
from datetime import datetime, timedelta


# run every 12  hours
def main():
    """
    Go through the users and see if they havnt been online in 3 days
    :return:
    """
    threedays = datetime.utcnow() - (timedelta(days=3))
    users = db.session.query(User).filter(User.last_seen <= threedays, User.id != 1).all()
    for user in users:

        # put user on vacation
        user.vacation = 1
        markitem = db.session.query(marketItem).filter_by(vendor_id=user.id).all()
        for item in markitem:
            item.online = 0
            db.session.add(item)
            db.session.add(user)

    db.session.commit()


def putonline():
    markitem = db.session.query(marketItem).filter_by(vendor_id=1).all()
    for item in markitem:
        item.online = 1
        db.session.add(item)

    db.session.commit()

main()
#putonline()