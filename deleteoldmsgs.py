from app import db

from app.classes.message import Post, Comment
from app.classes.service import shippingSecret, ReturnsTracking, websitefeedback

from datetime import datetime, timedelta

# run once a day
olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))


def deletereturnsshipping():
    """
    #this will delete all returns after 4 weeks
    :return:
    """

    getmsgs = db.session.query(ReturnsTracking).filter(ReturnsTracking.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deletesecretshipping():
    """
    #this will delete all secret shipping addresses after 4 weeks
    :return:
    """
    getmsgs = db.session.query(shippingSecret).filter(shippingSecret.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deleteoldmsgs():
    """
    #this deletes all message older than 10 weeks
    :return:
    """

    getmsgs = db.session.query(Post).filter(Post.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deleteoldmcomments():
    """
    #this deletes all comments older than 10 weeks
    :return:
    """
    getmsgs = db.session.query(Comment).filter(Comment.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()


def deleteoldfeedback():
    """
    # this deletes all feedback older than 10 weeks
    :return:
    """

    getmsgs = db.session.query(websitefeedback).filter(websitefeedback.timestamp < olderthanfourmonths).all()
    for f in getmsgs:
        db.session.delete(f)
    db.session.commit()



deleteoldmsgs()
deleteoldmcomments()
deletesecretshipping()
deleteoldfeedback()
deletereturnsshipping()