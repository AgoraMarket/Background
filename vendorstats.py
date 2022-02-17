from app import db
from app.classes.auth import Auth_User
from app.classes.userdata import UserData_Feedback
from app.classes.profile import Profile_StatisticsVendor
from decimal import Decimal
from sqlalchemy import func

# this script once a day


def vendorrating():
    """
    gets the vendor rating and item rating
    :return:
    """

    user = db.session.query(Auth_User).filter(Auth_User.vendor_account == 1).all()
    for f in user:
        vendorstats = db.session.query(Profile_StatisticsVendor).filter(f.id == Profile_StatisticsVendor.vendorid).first()
        if vendorstats:
            # gets average of vendor score
            getratingsvendor = db.session.query(func.avg(UserData_Feedback.vendorrating))
            getratingsvendor = getratingsvendor.filter(UserData_Feedback.vendorid == f.id)
            avgratevendor = getratingsvendor.all()
            vendorscore = (avgratevendor[0][0])

            if vendorscore is None:
                vendorscore = 0

            # gets average of item score
            getratingsitem = db.session.query(func.avg(UserData_Feedback.itemrating))
            getratingsitem = getratingsitem.filter(UserData_Feedback.vendorid == f.id, UserData_Feedback.itemrating != 0)
            avgrateitem = getratingsitem.all()
            itemscore = (avgrateitem[0][0])

            if itemscore is None:
                itemscore = 0

            # avg for vendor
            vendorstats.vendorrating = Decimal(vendorscore)
            # avg for item
            vendorstats.avgitemrating = Decimal(itemscore)

            db.session.add(vendorstats)
    db.session.commit()

vendorrating()



