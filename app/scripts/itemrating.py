from app import db
from sqlalchemy import func

from app.classes.item import Item_MarketItem
from app.classes.feedback import Feedback_Feedback

# this script once a day


def marketitemrating():
    """
    Gets all feedbacks
    finds how many
    finds average for an item
    :return:
    """
    
    change_order = False
    
    get_item = db.session\
        .query(Item_MarketItem)\
        .all()
        
    if get_item:
        for f in get_item:

            # count of how many
            getratings = db.session\
                .query(Feedback_Feedback)\
                .filter(Feedback_Feedback.item_uuid == f.uuid)\
                .count()

            # gets average of item score
            getratingsitem = db.session\
                .query(func.avg(Feedback_Feedback.item_rating))\
                .filter(Feedback_Feedback.item_uuid == f.uuid)\
                .all()
                
            # set score
            try:
                itemscore = (getratingsitem[0][0])
                if itemscore is None:
                    itemscore = 0
            except Exception as e:
                itemscore = 0

            # how many
            f.review_count = getratings
            # avg for item
            f.item_rating = itemscore

            # add item to db
            db.session.add(f)
            
            # update for commit
            change_order = True
            
                
        if change_order is True:
            db.session.commit()
            print("Updated ")
        else:
            print("No work done")




if __name__ == "__main__":
    marketitemrating()


