from app import db
from app.classes.item import Item_MarketItem
from decimal import Decimal


def turnoffmarketitems():
    markitem = db.session.query(Item_MarketItem).all()
    for specific_item in markitem:

        if specific_item.online == 1:
            # if not a proper profile image
            if len(specific_item.imageone) < 20:
                specific_item.online = 0
                db.session.add(specific_item)

            # not a proper country
            if specific_item.destinationcountry == 0:
                specific_item.online = 0
                db.session.add(specific_item)

            # needs origin country
            if specific_item.origincountry == 0:
                specific_item.online = 0
                db.session.add(specific_item)

            # shipping length greater than 1
            if len(specific_item.shippinginfo0) < 1:
                specific_item.online = 0
                db.session.add(specific_item)

            # item needs to be greater than 0
            if specific_item.itemcount <= 0:
                specific_item.online = 0
                db.session.add(specific_item)

            # needs price
            if Decimal(specific_item.price) < .000001:
                specific_item.online = 0
                db.session.add(specific_item)

            # item needs a title greater than 10
            if len(specific_item.itemtitlee) < 10:
                specific_item.online = 0
                db.session.add(specific_item)

            # if shipping two selected, needs price
            if specific_item.shippingtwo == 1:
                if Decimal(specific_item.shippingprice2) > .01:
                    if len(specific_item.shippinginfo2) >= 2:
                        pass
                else:
                    specific_item.shippingtwo = 0
                    db.session.add(specific_item)

            # if shipping three selected, needs price
            if specific_item.shippingthree == 1:
                if Decimal(specific_item.shippingprice3) > .01:
                    if len(specific_item.shippinginfo3) >= 2:
                        pass
                else:
                    specific_item.shippingthree = 0
                    db.session.add(specific_item)

    db.session.commit()


turnoffmarketitems()
