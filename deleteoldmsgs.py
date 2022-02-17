from app import db

from app.classes.message import Message_Post, Message_Comment
from app.classes.service import Service_ShippingSecret, Service_ReturnsTracking, Service_WebsiteFeedback

from datetime import datetime, timedelta

# run once a day
olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))


def deletereturnsshipping():
    """
    #this will delete all returns after 4 weeks
    :return:
    """

    getmsgs = db.session.query(Service_ReturnsTracking).filter(Service_ReturnsTracking.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deletesecretshipping():
    """
    #this will delete all secret shipping addresses after 4 weeks
    :return:
    """
    getmsgs = db.session.query(Service_ShippingSecret).filter(Service_ShippingSecret.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deleteoldmsgs():
    """
    #this deletes all message older than 10 weeks
    :return:
    """

    getmsgs = db.session.query(Message_Post).filter(Message_Post.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deleteoldmcomments():
    """
    #this deletes all comments older than 10 weeks
    :return:
    """
    getmsgs = db.session.query(Message_Comment).filter(Message_Comment.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deleteoldfeedback():
    """
    # this deletes all feedback older than 10 weeks
    :return:
    """

    getmsgs = db.session.query(Service_WebsiteFeedback).filter(Service_WebsiteFeedback.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()



deleteoldmsgs()
deleteoldmcomments()
deletesecretshipping()
deleteoldfeedback()
deletereturnsshipping()