from app import db
from app.classes.item import Item_MarketItem
from app.classes.user import Auth_User
from datetime import datetime, timedelta
from app.common.notification import create_notification
# run every 12 hours
def main():
    """
    Go through the users and see if they havnt been online in 2 days
    :return:
    """
    change_order = False
    
    two_days = datetime.utcnow() - (timedelta(days=2))
    
    users = db.session\
        .query(Auth_User)\
        .filter(Auth_User.last_seen <= two_days, Auth_User.id != 1)\
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
            # notify customer

        # notify vendor
        create_notification(
            username=user.user_name,
            user_uuid=user.uuid,
            msg='You have not logged in in 2 days.  All items have been turned off.'
        )
            
    if change_order is True:
        db.session.commit()
        print("Updated")
    else:
        print("No work done")


def putonline():
    """
    Puts EVERY item online.  Not a cron job currently
    """
    markitem = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.vendor_id == 1)\
        .all()
    for item in markitem:
        item.online = 1
        db.session.add(item)
        
    db.session.commit()

