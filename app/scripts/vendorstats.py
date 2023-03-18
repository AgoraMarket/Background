from app import db
from decimal import Decimal
from sqlalchemy import func
from app.classes.user import Auth_User
from app.classes.feedback import Feedback_Feedback
from app.classes.profile import Profile_StatisticsVendor

##
# this script once a day
# This Script calculates stats for the vendor.  It loops through all vendor
# accounts and gets item and vendor scores
##

def vendorrating():
    """
    gets the vendor rating and item rating
    :return:
    """

    user = db.session\
        .query(Auth_User)\
        .filter(Auth_User.vendor_account == 1)\
        .all()
    for f in user:
        # get vendor stats of user-
        vendorstats = db.session\
            .query(Profile_StatisticsVendor)\
            .filter(f.uuid == Profile_StatisticsVendor.vendor_uuid)\
            .first()

        if vendorstats:
            # gets average of vendor score
            getratingsvendor = db.session\
                .query(func.avg(Feedback_Feedback.vendor_rating))\
                .filter(Feedback_Feedback.vendor_uuid == f.uuid)\
                .all()

            # gets value of average from query
            vendorscore = (getratingsvendor[0][0])

            # set to 0 if no items found in query
            if vendorscore is None:
                vendorscore = 0

            # gets average of item score
            getratingsitem = db.session\
                .query(func.avg(Feedback_Feedback.item_rating))\
                .filter(Feedback_Feedback.vendor_uuid == f.uuid, Feedback_Feedback.item_rating != 0)\
                .all()
            itemscore = (getratingsitem[0][0])

            if itemscore is None:
                itemscore = 0

            # avg for vendor
            vendorstats.vendor_rating = Decimal(vendorscore)
            # avg for item
            vendorstats.avg_item_rating = Decimal(itemscore)

            db.session.add(vendorstats)

    db.session.commit()

