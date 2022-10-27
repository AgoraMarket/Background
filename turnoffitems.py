from app import db
from app.classes.item import Item_MarketItem
from app.classes.user import User
from datetime import datetime, timedelta


# run every 12 hours
def main():
    """
    Go through the users and see if they havnt been online in 2 days
    :return:
    """
    change_order = False
    two_days = datetime.utcnow() - (timedelta(days=2))
    users = db.session\
        .query(User)\
        .filter(User.last_seen <= two_days, User.id != 1)\
        .all()
    for user in users:
        change_order = True
        
        # put user on vacation
        user.vacation = 1
        
        # put there items on vacation
        markitem = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.vendor_id == user.id)\
            .all()
        
        db.session.add(user)
        
        # put items stuff online
        # loop in a loop very bad! Python Sucks
        for item in markitem:
            item.online = 0
            db.session.add(item)
           
            
    if change_order is True:
        db.session.commit()
        print("Updated")
    else:
        print("No work done")


def putonline():
    # put everything online
    markitem = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.vendor_id == 1)\
        .all()
    for item in markitem:
        item.online = 1
        db.session.add(item)
    db.session.commit()

main()
#putonline()