from app import db
from datetime import \
    datetime, \
    timedelta
from decimal import Decimal

# Models
from app.classes.vendor import Orders
from app.classes.auth import User
from app.classes.admin import AgoraFee
from app.classes.affiliate import AffiliateOverview

# End Models

from app.notification import \
    notification
from app.exppoints import \
    exppoint
from app.userdata.views import \
    addtotalItemsBought, \
    addtotalItemsSold, \
    totalspentonitems, \
    vendortotalmade, \
    affstats

from app.wallet_btccash.wallet_btccash_work import \
    btc_cash_sendCointoAgora, \
    btc_cash_sendcointoaffiliate, \
    btc_cash_sendCointoUser

##
# this script should run every hour
##


def markascompleted(itemid):
    item = Orders.query.get(id=itemid)
    item.completed = 1
    item.disputed_order = 0
    item.new_order = 0
    item.accepted_order = 0
    item.shipto_secretmsg = ''
    item.waiting_order = 0
    item.delivered_order = 1
    item.request_cancel = 0
    item.reason_cancel = 0
    item.request_return = 0
    item.cancelled = 0
    item.incart = 0
    item.modid = 0
    db.session.add(item)


def markascancelled(itemid):
    item = Orders.query.get(id=itemid)
    item.completed = 1
    item.disputed_order = 0
    item.new_order = 0
    item.accepted_order = 0
    item.waiting_order = 0
    item.delivered_order = 1
    item.request_cancel = 0
    item.reason_cancel = 0
    item.request_return = 0
    item.cancelled = 1
    item.shipto_secretmsg = ''
    item.incart = 0
    item.modid = 0
    db.session.add(item)


def neworders_48hours():
    """
    #this function is if the vendor didnt accepted in 48 hours. cancels gives back to customer
    :return:
    """

    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.type == 1)
    acceptedorders = acceptedorders.filter(Orders.new_order == 1)
    aorders = acceptedorders.all()
    for f in aorders:
        whenbought = f.age
        itemprice = Decimal(f.price)
        shipprice = Decimal(f.shipping_price)
        totalprice = Decimal(itemprice + shipprice)
        comment = "Vendor accept expired. Automatic refund for order number " + str(f.id)
        twoday = (whenbought + timedelta(days=2))
        if datetime.utcnow() > twoday:
            # Order wasnt accepted in time=.  Give money back to customer

            # this function adds the work to db
            btc_cash_sendCointoUser(amount=totalprice,
                                   comment=comment,
                                   userid=f.customer_id)

            # notify customer
            notification(type=6,
                         username=f.customer,
                         userid=f.customer_id,
                         salenumber=f.id,
                         bitcoin=f.totalprice)

            # notify vendor
            notification(type=6,
                         username=f.vendor,
                         userid=f.vendor_id,
                         salenumber=f.id,
                         bitcoin=f.totalprice)

            markascancelled(itemid=f.id)

    db.session.commit()


def acceptedorders_1week():
    """
    #this function is for if the vendor didnt ship after 1 week. Cancel give back to customer
    :return:
    """
    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.type == 1)
    acceptedorders = acceptedorders.filter(Orders.accepted_order == 1)
    aorders = acceptedorders.all()
    for f in aorders:
        whenbought = f.age
        itemprice = Decimal(f.price)
        shipprice = Decimal(f.shipping_price)
        totalprice = Decimal(itemprice + shipprice)
        comment = "Vendor didnt ship in time. Automatic refund for order number " + str(f.id)
        nextday = (whenbought + timedelta(days=7))
        if datetime.utcnow() > nextday:
            # Order was accepted but not shipped..return back to customer

            # this function adds the work to db
            btc_cash_sendCointoUser(amount=totalprice,
                           comment=comment,
                           userid=f.customer_id)

            # notify customer
            notification(type=6,
                         username=f.customer,
                         userid=f.customer_id,
                         salenumber=f.id,
                         bitcoin=f.totalprice)

            # notify vendor
            notification(type=6,
                         username=f.vendor,
                         userid=f.vendor_id,
                         salenumber=f.id,
                         bitcoin=f.totalprice)

            markascancelled(itemid=f.id)

    db.session.commit()


def requestcancel_24rs():
    """
    # this function is if customer requests return,
    but vendor hasn't responded in 24 hrs.
    auto cancels and refunds user
    :return:
    """
    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.type == 0)
    acceptedorders = acceptedorders.filter(Orders.request_cancel == 1)
    aorders = acceptedorders.all()

    for accorder in aorders:
        whenrequested = accorder.returncancelage
        itemprice = Decimal(accorder.price)
        shipprice = Decimal(accorder.shipping_price)
        totalprice = Decimal(itemprice + shipprice)
        comment = "Order was canceled. Order#" + str(accorder.id)

        nextday = (whenrequested + timedelta(days=1))
        if datetime.utcnow() > nextday:
            # Order was accepted but not shipped..return back to customer
            # this function adds the work to db
            btc_cash_sendCointoUser(amount=totalprice,
                           comment=comment,
                           userid=accorder.customer_id)

            # notify customer
            notification(type=6,
                         username=accorder.customer,
                         userid=accorder.customer_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            # notify vendor
            notification(type=6,
                         username=accorder.vendor,
                         userid=accorder.vendor_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            markascancelled(itemid=accorder.id)
    db.session.commit()


def returns_2days():
    """

    # after a return is initiated, the vendor has 2 days to provide a return address.
     If not vendor keeps money
    :return:
    """
    # request return is 2
    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.request_return == 2)
    acceptedorders = acceptedorders.filter(Orders.type == 1)
    aorders = acceptedorders.all()

    for accorder in aorders:
        whenrequested = accorder.returncancelage
        itemprice = Decimal(accorder.price)
        shipprice = Decimal(accorder.shipping_price)
        totalprice = Decimal(itemprice + shipprice)
        comment = "Return time expired for order#:" + str(accorder.id)
        sevenday = (whenrequested + timedelta(days=2))
        if datetime.utcnow() > sevenday:

            # Autofinalize so give to vendor
            btc_cash_sendCointoUser(amount=totalprice,
                           comment=comment,
                           userid=accorder.vendor_id)

            # notify customer
            notification(type=6,
                         username=accorder.customer,
                         userid=accorder.customer_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            # notify vendor
            notification(type=6,
                         username=accorder.vendor,
                         userid=accorder.vendor_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            markascompleted(itemid=accorder.id)
    db.session.commit()


def returns_7days():
    """
    # the customer has 7 days to mark as returned after/if vendor provided return.
    # If not vendor keeps money
    :return:
    """
    # request return is 2
    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.request_return == 2)
    acceptedorders = acceptedorders.filter(Orders.type == 1)
    aorders = acceptedorders.all()

    for accorder in aorders:
        whenrequested = accorder.returncancelage
        itemprice = Decimal(accorder.price)
        shipprice = Decimal(accorder.shipping_price)
        totalprice = Decimal(itemprice + shipprice)
        comment = "Return time expired for order#:" + str(accorder.id)
        sevenday = (whenrequested + timedelta(days=7))
        if datetime.utcnow() > sevenday:

            # Autofinalize so give to vendor
            btc_cash_sendCointoUser(amount=totalprice,
                           comment=comment,
                           userid=accorder.vendor_id)

            # notify customer
            notification(type=6,
                         username=accorder.customer,
                         userid=accorder.customer_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            # notify vendor
            notification(type=6,
                         username=accorder.vendor,
                         userid=accorder.vendor_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            markascompleted(itemid=accorder.id)

    db.session.commit()


def returns_14days():
    """
    #after a return is marked as shipped by customer, vendor gets money in 14 days.  If not
    :return:
    """
    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.request_return == 3)
    acceptedorders = acceptedorders.filter(Orders.type == 1)
    aorders = acceptedorders.all()

    for accorder in aorders:
        whenreturned = accorder.returncancelage
        itemprice = Decimal(accorder.price)
        shipprice = Decimal(accorder.shipping_price)
        totalprice = Decimal(itemprice + shipprice)
        comment = "Return for order#:" + str(accorder.id)
        nextday = (whenreturned + timedelta(days=14))
        if datetime.utcnow() > nextday:

            # Autofinalize so give to user
            btc_cash_sendCointoUser(amount=totalprice,
                           comment=comment,
                           userid=accorder.customer_id)

            # notify customer
            notification(type=6,
                         username=accorder.customer,
                         userid=accorder.customer_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            # notify vendor
            notification(type=6,
                         username=accorder.vendor,
                         userid=accorder.vendor_id,
                         salenumber=accorder.id,
                         bitcoin=accorder.totalprice)

            markascompleted(itemid=accorder.id)

    db.session.commit()


def autofinalize_30days():
    """
    #this function gives the money to the vendor after 30 days if no issues
    :return:
    """
    # get the current fee
    currentfee = AgoraFee.query.filter_by(id=1).first()
    physicalitemfee = currentfee.itempurchase

    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 0)
    acceptedorders = acceptedorders.filter(Orders.type == 1)
    acceptedorders = acceptedorders.filter(Orders.waiting_order == 1)
    acceptedorders = acceptedorders.filter(Orders.disputed_order == 0)
    acceptedorders = acceptedorders.filter(Orders.request_return == 0)
    aorders = acceptedorders.all()

    for order_to_be_finalized in aorders:
        getcustomer = db.session.query(User).filter(User.id == order_to_be_finalized.customer_id).first()
        whenbought = order_to_be_finalized.age
        itemprice = Decimal(order_to_be_finalized.price)
        shipprice = Decimal(order_to_be_finalized.shipping_price)
        thefee = Decimal(order_to_be_finalized.fee)
        totalprice = Decimal(itemprice + shipprice) - thefee

        thirtydaysfromorder = (whenbought + timedelta(days=30))
        if datetime.utcnow() > thirtydaysfromorder:

            # BTC
            if order_to_be_finalized.digital_currency == 2:
                if order_to_be_finalized.affiliate_code != 0 and order_to_be_finalized.affiliate_discount_percent != 0:
                    # split the profit and how much affiliate gets

                    getpromo = db.session.query(AffiliateOverview) \
                        .filter(AffiliateOverview.promocode == order_to_be_finalized.affiliate_code).first()

                    # variables
                    promopercent = (Decimal(getpromo.aff_fee / 100))
                    amounttomodify = (Decimal(order_to_be_finalized.price_beforediscount))

                    # percent for affiliate
                    # multiply amount before fee off *  promo percent
                    amount_to_affiliate = (amounttomodify * promopercent)

                    # percent to protos
                    # physicalfeefor item - feeforaffiliate == feeforprotos
                    feeforprotos = physicalitemfee - promopercent
                    if feeforprotos < 0:
                        feeforprotos = 0
                    else:
                        feeforprotos = feeforprotos

                    #  amounttomnodify * feeforprotos
                    amount_to_protos = amounttomodify * feeforprotos

                    # order the amount sent
                    btc_cash_sendcointoaffiliate(amount=amount_to_affiliate,
                                                 comment=order_to_be_finalized.id,
                                                 userid=getpromo.userid)

                    # amount = fee - affiliate fee
                    btc_cash_sendCointoAgora(amount=amount_to_protos,
                                            comment=order_to_be_finalized.id,
                                            shard=getcustomer.shard)

                    # add affiliate stats
                    affstats(userid=getpromo.userid,
                             amount=amount_to_affiliate,
                             currency=2)

                else:
                    # send normal fee- BTC
                    btc_cash_sendCointoAgora(amount=thefee,
                                             comment=order_to_be_finalized.id,
                                             shard=getcustomer.shard)

                # Autofinalize so give to vendor
                # send price + shipping
                btc_cash_sendCointoUser(amount=totalprice,
                                        comment=order_to_be_finalized.id,
                                        userid=order_to_be_finalized.vendor_id)

            # BTC Cash
            else:

                # split the profit and how much affiliate gets
                if order_to_be_finalized.affiliate_code != 0 and order_to_be_finalized.affiliate_discount_percent != 0:
                    getpromo = db.session.query(AffiliateOverview) \
                        .filter(AffiliateOverview.promocode == order_to_be_finalized.affiliate_code)\
                        .first()

                    # variables
                    promopercent = (Decimal(getpromo.aff_fee / 100))
                    amounttomodify = (Decimal(order_to_be_finalized.price_beforediscount))

                    # percent for affiliate
                    # multiply amount before fee off *  promo percent
                    amount_to_affiliate = (amounttomodify * promopercent)

                    # percent to protos
                    # physicalfeefor item - feeforaffiliate == feeforprotos
                    feeforprotos = physicalitemfee - promopercent
                    if feeforprotos < 0:
                        feeforprotos = 0
                    else:
                        feeforprotos = feeforprotos
                    #  amounttomnodify * feeforprotos
                    amount_to_protos = amounttomodify * feeforprotos

                    # percennt to affiliate
                    btc_cash_sendcointoaffiliate(amount=amount_to_affiliate,
                                                 comment=order_to_be_finalized.id,
                                                 userid=getpromo.userid)

                    # percent to protoss
                    btc_cash_sendCointoAgora(amount=amount_to_protos,
                                             comment=order_to_be_finalized.id,
                                             shard=getcustomer.shard)

                    # add affiliate stats
                    affstats(userid=getpromo.userid,
                             amount=amount_to_affiliate,
                             currency=2)

                else:
                    # percent to protoss
                    btc_cash_sendCointoAgora(amount=thefee,
                                             comment=order_to_be_finalized.id,
                                             shard=getcustomer.shard)

                # Autofinalize so give to vendor - BTC CASH
                btc_cash_sendCointoUser(amount=totalprice,
                                        comment=order_to_be_finalized.id,
                                        userid=order_to_be_finalized.vendor_id)

            # notify vendor
            notification(type=6,
                         username=order_to_be_finalized.vendor,
                         userid=order_to_be_finalized.vendor_id,
                         salenumber=order_to_be_finalized.id,
                         bitcoin=totalprice)

            # mark as completed
            markascompleted(itemid=order_to_be_finalized.id)

            # add stats
            # Add total items bought
            addtotalItemsBought(userid=order_to_be_finalized.customer_id,
                                howmany=order_to_be_finalized.quantity)

            # add total sold to vendor
            addtotalItemsSold(userid=order_to_be_finalized.vendor_id,
                              howmany=order_to_be_finalized.quantity)

            # BTC Spent by user
            totalspentonitems(userid=order_to_be_finalized.customer_id,
                              howmany=order_to_be_finalized.quantity,
                              amount=order_to_be_finalized.price)

            # BTC recieved by vendor
            vendortotalmade(userid=order_to_be_finalized.vendor_id,
                            amount=order_to_be_finalized.price)

            # Give Vendor experience points
            exppoint(user=order_to_be_finalized.vendor_id,
                     price=order_to_be_finalized.price,
                     type=11,
                     quantity=order_to_be_finalized.quantity,
                     currency=order_to_be_finalized.currency)

            # Give user experience points
            exppoint(user=order_to_be_finalized.customer_id,
                     price=order_to_be_finalized.price,
                     type=1,
                     quantity=order_to_be_finalized.quantity,
                     currency=order_to_be_finalized.currency)

    db.session.commit()


requestcancel_24rs()
neworders_48hours()
acceptedorders_1week()
autofinalize_30days()
returns_7days()
returns_14days()
