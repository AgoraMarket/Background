from app import db
from app.classes.item import Item_MarketItem
from decimal import Decimal


def turnoffmarketitems():
    change_order = False
    markitem = db.session\
        .query(Item_MarketItem)\
        .all()
    for specific_item in markitem:
        try:
            if specific_item.online == 1:
                
                # if not a proper profile image
                if len(specific_item.image_one_server) < 10:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True
                # not a proper country
                if specific_item.destination_country_one == 0:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True
                # needs origin country
                if specific_item.origin_country == 0:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True
                # shipping length greater than 1
                if len(specific_item.shipping_info_0) < 1:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True
                # item needs to be greater than 0
                if specific_item.item_count <= 0:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True
                # needs price
                if Decimal(specific_item.price) < .000001:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True

                # item needs a title greater than 10
                if len(specific_item.item_title) < 10:
                    specific_item.online = 0
                    db.session.add(specific_item)
                    change_order = True

                # if shipping two selected, needs price
                if specific_item.shipping_two is True:
                    
                    if Decimal(specific_item.shipping_price_2) > .01:
                        if len(specific_item.shipping_info_2) >= 2:
                            pass
                    else:
                        specific_item.shipping_two = False
                        db.session.add(specific_item)
                        change_order = True

                # if shipping three selected, needs price
                if specific_item.shipping_three is True:
                    if Decimal(specific_item.shipping_price_3) > .01:
                        if len(specific_item.shipping_info_3) >= 2:
                            pass
                    else:
                        specific_item.shipping_three = False
                        db.session.add(specific_item)
                        change_order = True
        except Exception as e:
            print(str(e))
            continue
            

    if change_order is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")


