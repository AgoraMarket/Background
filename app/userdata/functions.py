import os


from app import db
from decimal import Decimal
from app import UPLOADED_FILES_DEST_USER

# models
from app.classes.user import User
from app.classes.profile import\
Profile_StatisticsUser,\
Profile_StatisticsVendor
# End Models

from app.common.functions import\
mkdir_p,\
userimagelocation,\
convert_to_local_bch,\
convert_to_local_btc,\
convert_to_local_xmr





def userdata_add_total_items_sold(user_id, howmany):
    """
    how many items a customer sold
    """""

    itemssold = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()

    a = itemssold.total_sales
    x = int(a) + int(howmany)

    itemssold.total_sales = x

    db.session.add(itemssold)



def userdata_add_total_items_bought(user_id, howmany):
    """
    Total items bought by a user
    :param user_id:
    :param howmany:
    :return:
    """
    # how many items a customer bought
    items_bought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()

    a = items_bought.total_items_bought
    x = a + howmany
    items_bought.total_items_bought = x
    db.session.add(items_bought)



def userdata_add_total_trades_user(user_id):
    """
    How many trades a customer did
    """
    userstats = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    useramount = userstats.total_trades
    usernewamount = useramount + 1
    userstats.total_trades = usernewamount

    db.session.add(userstats)
    db.session.commit()




def userdata_add_total_trades_vendor(user_id):
    # how many trades a customer did
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    # add total trades to vendor
    amount = vendorstats.total_trades
    newamount = amount + 1
    vendorstats.total_trades = newamount

    db.session.add(vendorstats)




def userdata_different_trading_partners_user(user_id, otherid):
    # adds diff partners to user file
    # get customer txt and write vendor id
    ##
    user = db.session\
        .query(User)\
        .filter(user_id == User.id)\
        .first()

    itemsbought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    # find path of the user
    getuserlocation = userimagelocation(user_id=user.id)
    thepath = os.path.join(UPLOADED_FILES_DEST_USER,getuserlocation, str(user_id))
    # make a directory if doesnt have it..should tho
    mkdir_p(path=thepath)
    # text file is user_id
    usertextfile = str(user.id) + ".txt"
    # text file location
    userfile = os.path.join(thepath, usertextfile)
    # vendor trade log
    othertraderid = str(otherid)
    text_file = open(userfile, "a")
    f = open(userfile, 'r')
    x = set(f.read().split(','))
    if str(otherid) in x:
        y = (len(x)) - 1
        itemsbought.diff_partners = y
    else:
        text_file.write(othertraderid + ',')
        text_file.close()
        y = (len(x))
        itemsbought.diffpartners = y

    db.session.add(itemsbought)


def userdata_different_trading_partners_vendor(user_id, otherid):
    """
    # adds diff partners to user file
    # get vendor txt and write customer id
    :param user_id:
    :param otherid:
    :return:
    """
    # get the user
    user = db.session\
        .query(User)\
        .filter(user_id == User.id)\
        .first()
    getuserlocation = userimagelocation(user_id=user.id)
    # get stats if vendor
    itemsbought = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    # find path of the user
    thepath = os.path.join(UPLOADED_FILES_DEST_USER,
                           getuserlocation, str(user.id))
    # make a directory if doesnt have it..should tho
    mkdir_p(path=thepath)
    # text file is user_id
    usertextfile = str(user.id) + ".txt"
    # text file location
    userfile = os.path.join(thepath, usertextfile)
    # get the other persons id
    othertraderid = str(otherid)
    text_file = open(userfile, "a")
    f = open(userfile, 'r')
    x = set(f.read().split(','))
    if str(otherid) in x:
        y = (len(x)) - 1
        itemsbought.diff_partners = y
    else:
        text_file.write(othertraderid + ',')
        text_file.close()
        y = (len(x))
        itemsbought.diff_partners = y

    db.session.add(itemsbought)


def userdata_reviews_given(user_id):
    """
    # adds a review given by user
    :param user_id:
    :return:
    """

    review_stats = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    y = review_stats.total_reviews
    x = y + 1
    review_stats.total_reviews = x

    db.session.add(review_stats)


def userdata_reviews_recieved(user_id):
    """
    # adds a review recieved as a vendor
    :param user_id:
    :return:
    """

    review_stats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    y = review_stats.total_reviews
    x = y + 1
    review_stats.total_reviews = x

    db.session.add(review_stats)


def userdata_add_flag(user_id):
    # adds a flag to user stats
    review_stats = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    y = review_stats.items_flagged
    x = y + 1
    review_stats.items_flagged = x

    db.session.add(review_stats)


def userdata_vendor_flag(user_id):
    # adds a flag to vendor stats
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    # add total trades to vendor
    amount = vendorstats.been_flagged
    newamount = amount + 1
    vendorstats.been_flagged = newamount

    db.session.add(vendorstats)

# bitcoin cash
def userdata_total_spent_on_item_bch(user_id, amount, howmany):
    # USER
    # how much money a user has spent of physical items
    
    itemsbought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    a = itemsbought.total_bch_spent
    if a is None:
        a = 0
    totalamt = (Decimal(amount) * int(howmany))
    x = (Decimal(a + totalamt))
    itemsbought.total_bch_spent = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_bch(amount=amount, currency=0)
    addmount = itemsbought.total_usd_spent + amountinusd
    itemsbought.total_usd_spent = addmount

    db.session.add(itemsbought)

# bitcoin cash
def userdata_total_made_on_item_bch(user_id, amount):
    # vendor
    # how much money a user has spent of physical items
    # bitcoin cash
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    a = vendorstats.total_bch_recieved
    if a is None:
        a = 0
    x = (Decimal(a + amount))
    vendorstats.total_bch_recieved = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_bch(amount=amount, currency=0)
    addmount = vendorstats.total_usd_made + amountinusd
    vendorstats.total_usd_made = addmount

    db.session.add(vendorstats)


# bitcoin
def userdata_total_spent_on_item_btc(user_id, amount, howmany):
    # USER
    # how much money a user has spent of physical items
 
    itemsbought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    a = itemsbought.total_btc_spent
    if a is None:
        a = 0
    totalamt = (Decimal(amount) * int(howmany))
    x = (Decimal(a + totalamt))
    itemsbought.total_btc_spent = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_btc(amount=amount, currency=0)
    addmount = itemsbought.total_usd_spent + amountinusd
    itemsbought.total_usd_spent = addmount

    db.session.add(itemsbought)

# bitcoin
def userdata_total_made_on_item_btc(user_id, amount):
    # vendor
    # how much money a user has spent of physical items
    # bitcoin 
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    a = vendorstats.total_btc_recieved
    if a is None:
        a = 0
    x = (Decimal(a + amount))
    vendorstats.total_btc_recieved = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_btc(amount=amount, currency=0)
    addmount = vendorstats.total_usd_made + amountinusd
    vendorstats.total_usd_made = addmount

    db.session.add(vendorstats)


# Monero
def userdata_total_spent_on_item_xmr(user_id, amount, howmany):
    # USER
    # how much money a user has spent of physical items
    itemsbought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_uuid)\
        .first()
    a = itemsbought.total_xmr_spent
    if a is None:
        a = 0
    totalamt = (Decimal(amount) * int(howmany))
    x = (Decimal(a + totalamt))
    itemsbought.total_xmr_spent = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_xmr(amount=amount, currency=0)
    addmount = itemsbought.total_usd_spent + amountinusd
    itemsbought.total_usd_spent = addmount

    db.session.add(itemsbought)

# Monero
def userdata_total_made_on_item_xmr(user_id, amount):
    # vendor
    # how much money a user has spent of physical items
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendor_uuid)\
        .first()
    a = vendorstats.total_xmr_recieved
    if a is None:
        a = 0
    x = (Decimal(a + amount))
    vendorstats.total_xmr_recieved = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_xmr(amount=amount, currency=0)
    addmount = vendorstats.total_usd_made + amountinusd
    vendorstats.total_usd_made = addmount

    db.session.add(vendorstats)




