from app import db
from app.classes.auth import Auth_User
from app.classes.profile import Profile_Userreviews, Profile_StatisticsUser
from decimal import Decimal
from sqlalchemy import func

# this script once a day


def userrating():
    user = db.session.query(Auth_User).all()
    for f in user:
        userstats = db.session.query(Profile_StatisticsUser).filter(f.id == Profile_StatisticsUser.user_id).first()
        if userstats:
            # gets avg
            getratings = db.session.query(func.avg(Profile_Userreviews.rating))
            getratings = getratings.filter(Profile_Userreviews.customer_id == f.id)
            avgrate = getratings.all()
            # take avg to a decimal
            try:
                itemscore = (avgrate[0][0])

                if itemscore is None:
                    itemscore = 0
            except:
                itemscore = 0

            # add user stats to db
            userstats.userrating = Decimal(itemscore)
            db.session.add(userstats)
    db.session.commit()

userrating()
