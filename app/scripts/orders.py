from app import db
from datetime import \
    datetime, \
    timedelta
from sqlalchemy import or_

# Models
from app.classes.user_orders import User_Orders

# End Models
from app.notification import notification

from app.userdata.functions import \
    userdata_add_total_items_bought, \
    userdata_add_total_items_sold, \
    userdata_total_spent_on_item_btc, \
    userdata_total_made_on_item_btc, \
    userdata_total_spent_on_item_bch, \
    userdata_total_made_on_item_bch, \
    userdata_total_spent_on_item_xmr, \
    userdata_total_made_on_item_xmr

from app.wallet_bch.wallet_bch_work import\
    finalize_order_bch,\
    bch_send_coin_to_user

from app.wallet_btc.wallet_btc_work import\
    finalize_order_btc,\
    btc_send_coin_to_user

from app.wallet_xmr.wallet_xmr_work import\
    finalize_order_xmr,\
    xmr_send_coin_to_user


##
# this script should run every hour
# Its purpose to finalize waiting orders
##
"""
1. fresh order not accepted
2. accepted
3. shipped
4. delivered
6. Request Cancel
7. Cancelled
8. disputed
10. finalized
"""
def neworders_48hours():
    """
    # This function is if the vendor didnt accepted in 48 hours. Cancel give back to customer
    :return:
    """
    # if change order is true add to db
    change_order = False
    
    acceptedorders = db.session\
        .query(User_Orders)\
        .filter(User_Orders.overall_status == 1)\
        .all()

    for f in acceptedorders:

        whenbought = f.created
        twoday = (whenbought + timedelta(days=2))

        if datetime.utcnow() > twoday:
            # Order was not accepted in time.  Give money back to customer
            # BTC
            if f.digital_currency == 1:
                btc_send_coin_to_user(amount=f.price_total_btc,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )

            elif f.digital_currency == 2:
                bch_send_coin_to_user(amount=f.price_total_bch,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )

            elif f.digital_currency == 3:
                xmr_send_coin_to_user(amount=f.price_total_xmr,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )


            # notify customer
            notification(type=6,
                         username=f.customer_user_name,
                         user_id=f.customer_id,
                         salenumber=f.uuid,
                         bitcoin=f.totalprice)

            # notify vendor
            notification(type=6,
                         username=f.vendor_user_name,
                         user_id=f.vendor_id,
                         salenumber=f.uuid,
                         bitcoin=f.totalprice)

            f.overall_status = 6

            change_order = True

    if change_order is True:
        db.session.commit()

def acceptedorders_1week():
    """
    #this function is for if the vendor didnt ship after 1 week. Cancel give back to customer
    :return:
    """

    change_order = False

    acceptedorders = db.session\
        .query(User_Orders)\
        .filter(User_Orders.overall_status == 2)\
        .all()

    for f in acceptedorders:

        whenbought = f.created
        nextday = (whenbought + timedelta(days=5))

        if datetime.utcnow() > nextday:
            # Order was accepted but not shipped. Give back to customer

            if f.digital_currency == 1:
                btc_send_coin_to_user(amount=f.price_total_btc,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )
                
                notification(type=6,
                            username=f.customer_user_name,
                            user_id=f.customer_id,
                            salenumber=f.uuid,
                            bitcoin=f.price_total_btc)

                # notify vendor
                notification(type=6,
                            username=f.vendor_user_name,
                            user_id=f.vendor_id,
                            salenumber=f.uuid,
                            bitcoin=f.price_total_btc)

            elif f.digital_currency == 2:
                bch_send_coin_to_user(amount=f.price_total_bch,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )
                notification(type=6,
                            username=f.customer_user_name,
                            user_id=f.customer_id,
                            salenumber=f.uuid,
                            bitcoin=f.price_total_bch)

                # notify vendor
                notification(type=6,
                            username=f.vendor_user_name,
                            user_id=f.vendor_id,
                            salenumber=f.uuid,
                            bitcoin=f.price_total_bch)

            elif f.digital_currency == 3:
                xmr_send_coin_to_user(amount=f.price_total_xmr,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )
                notification(type=6,
                            username=f.customer_user_name,
                            user_id=f.customer_id,
                            salenumber=f.uuid,
                            bitcoin=f.price_total_xmr
                             )

                # notify vendor
                notification(type=6,
                            username=f.vendor_user_name,
                            user_id=f.vendor_id,
                            salenumber=f.uuid,
                            bitcoin=f.price_total_xmr
                            )
        
            f.overall_status = 6

            change_order = True

    if change_order is True:
        db.session.commit()


def requestcancel_24rs():
    """
    # this function is if customer requests return,
    but vendor hasn't responded in 24 hrs.
    auto cancels and refunds user
    :return:
    """

    change_order = False

    acceptedorders = db.session\
        .query(User_Orders)\
        .filter(User_Orders.overall_status == 6)\
        .all()

    for f in acceptedorders:

        whenrequested = f.returncancelage
        nextday = (whenrequested + timedelta(days=1))

        if datetime.utcnow() > nextday:

            if f.digital_currency == 1:
                btc_send_coin_to_user(amount=f.price_total_btc,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )

            elif f.digital_currency == 2:
                bch_send_coin_to_user(amount=f.price_total_bch,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )

            elif f.digital_currency == 3:
                xmr_send_coin_to_user(amount=f.price_total_xmr,
                                      user_id=f.customer_id,
                                      order_uuid=f.uuid
                                      )

            # notify customer
            notification(type=6,
                         username=f.customer_user_name,
                         user_id=f.customer_id,
                         salenumber=f.uuid,
                         bitcoin=f.totalprice)

            # notify vendor
            notification(type=6,
                         username=f.vendor_user_name,
                         user_id=f.vendor_id,
                         salenumber=f.uuid,
                         bitcoin=f.totalprice)

            f.overall_status = 6

            change_order = True

    if change_order is True:
        print("updated orders")
        db.session.commit()


def autofinalize_20days():
    """
    #this function gives the money to the vendor after 30 days if no issues
    :return:
    """
    # get the current fee

    change_order = False

    acceptedorders = db.session\
        .query(User_Orders)\
        .filter(or_(User_Orders.overall_status == 3, User_Orders.overall_status == 4))\
        .all()

    for f in acceptedorders:

        whenbought = f.created
        twentydaysfromorder = (whenbought + timedelta(days=20))

        if datetime.utcnow() > twentydaysfromorder:

            # BTC
            if f.digital_currency == 1:
                # finalize order
                finalize_order_bch(f.uuid)
                
                # notify vendor
                notification(type=6,
                             username=f.vendor_user_name,
                             user_id=f.vendor_id,
                             salenumber=f.uuid,
                             bitcoin=f.price_total_btc)
                
                # calculate amount for stats
                total_made_sale = f.price_total_bch - f.shipping_price_btc
                
                # Bch Spent by user
                userdata_total_spent_on_item_btc(user_id=f.customer_uuid,
                                                howmany=f.quantity,
                                                amount=f.total_made_sale)

                # Bch recieved by vendor
                userdata_total_made_on_item_btc(user_id=f.vendor_uuid,
                                                 amount=f.total_made_sale)
            # BTC Cash
            elif f.digital_currency == 2:
                # finalize order
                finalize_order_btc(f.uuid)
                
                # notify vendor
                notification(type=6,
                             username=f.vendor_user_name,
                             user_id=f.vendor_id,
                             salenumber=f.uuid,
                             bitcoin=f.price_total_bch)
                
                # calculate amount for stats
                total_made_sale = f.price_total_bch - f.shipping_price_btc
                
                # Bch Spent by user
                userdata_total_spent_on_item_bch(user_id=f.customer_uuid,
                                                howmany=f.quantity,
                                                amount=f.total_made_sale)

                # Bch recieved by vendor
                userdata_total_made_on_item_bch(user_id=f.vendor_uuid,
                                            amount=f.total_made_sale)
            # XMR
            elif f.digital_currency == 3:
                
                # finalize order
                finalize_order_xmr(f.uuid)
                
                # notify vendor
                notification(type=6,
                             username=f.vendor_user_name,
                             user_id=f.vendor_id,
                             salenumber=f.uuid,
                             bitcoin=f.price_total_xmr)
                
                # calculate amount for stats
                total_made_sale = f.price_total_bch - f.shipping_price_btc
                
                # xmr Spent by user
                userdata_total_spent_on_item_xmr(user_id=f.customer_uuid,
                                                howmany=f.quantity,
                                                amount=total_made_sale)

                # xmr recieved by vendor
                userdata_total_made_on_item_xmr(user_id=f.vendor_uuid,
                                                amount=total_made_sale)

            else:
                break


            # add stats
            # Add total items bought
            userdata_add_total_items_bought(user_id=f.customer_uuid,
                                            howmany=f.quantity)

            # add total sold to vendor
            userdata_add_total_items_sold(user_id=f.vendor_uuid,
                                          howmany=f.quantity)

       

            f.overall_status = 10

            change_order = True

    if change_order is True:
        db.session.commit()
        print("Updated Orders")
    else:
        print("No work done")


