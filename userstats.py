from app import db
from app.classes.auth import User
from app.classes.profile import Userreviews, StatisticsUser
from decimal import Decimal
from sqlalchemy import func

# this script once a day


def userrating():
    user = db.session.query(User).all()
    for f in user:
        userstats = db.session.query(StatisticsUser).filter(f.id == StatisticsUser.usernameid).first()
        if userstats:
            # gets avg
            getratings = db.session.query(func.avg(Userreviews.rating))
            getratings = getratings.filter(Userreviews.customer_id == f.id)
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
