from app import db
from app.classes.user import User
from app.classes.profile import  Profile_StatisticsUser
from app.classes.feedback import Feedback_Feedback
from decimal import Decimal
from sqlalchemy import func

# this script once a day


def userrating():
    change_order = False
    user = db.session\
        .query(User)\
        .all()
    for f in user:
        # get stats to user
        userstats = db.session\
            .query(Profile_StatisticsUser)\
            .filter(f.uuid == Profile_StatisticsUser.user_uuid)\
            .first()
        if userstats:
            
            # gets avg from query
            getratings = db.session\
                .query(func.avg(Feedback_Feedback.customer_rating))\
                .filter(Feedback_Feedback.customer_uuid == f.uuid)\
                .all()
                
            # take avg to a decimal
            try:
                itemscore = (getratings[0][0])
                if itemscore is None:
                    itemscore = 0
            except:
                itemscore = 0
                
            # set score
            userstats.user_rating = Decimal(itemscore)
            
            # add user stats to db
            db.session.add(userstats)
            change_order = True
    if change_order is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")


userrating()
