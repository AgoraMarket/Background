from app import db

from app.classes.message import \
    Message_Post, Message_Chat
from app.classes.service import \
    Service_ShippingSecret,\
    Service_ReturnsTracking,\
    Service_WebsiteFeedback

from datetime import datetime, timedelta

# run once a day

def deletereturnsshipping():
    """
    #this will delete all returns after 4 weeks
    :return:
    """
    olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))

    updated_info = False
    
    getmsgs = db.session\
        .query(Service_ReturnsTracking)\
        .filter(Service_ReturnsTracking.timestamp < olderthanfourmonths)\
        .all()
    for f in getmsgs:
        db.session.delete(f)
        updated_info = True

    if updated_info is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")



def deletesecretshipping():
    """
    #this will delete all secret shipping addresses after 4 weeks
    :return:
    """
    olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))

    updated_info = False
    
    getmsgs = db.session\
        .query(Service_ShippingSecret)\
        .filter(Service_ShippingSecret.timestamp < olderthanfourmonths)\
        .all()
    for f in getmsgs:
        db.session.delete(f)
        updated_info = True

    if updated_info is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")

def deleteoldmsgs():
    """
    #this deletes all message older than 10 weeks
    :return:
    """
    updated_info = False
    
    olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))


    getmsgs = db.session\
        .query(Message_Post)\
        .filter(Message_Post.timestamp < olderthanfourmonths)\
        .all()
    for f in getmsgs:
        db.session.delete(f)
        updated_info = True

    if updated_info is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")

def deleteoldmcomments():
    """
    #this deletes all comments older than 10 weeks
    :return:
    """
    updated_info = False
    
    olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))


    getmsgs = db.session\
        .query(Message_Chat)\
        .filter(Message_Chat.timestamp < olderthanfourmonths)\
        .all()
    for f in getmsgs:
        db.session.delete(f)
        updated_info = True

    if updated_info is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")

def deleteoldfeedback():
    """
    # this deletes all feedback older than 10 weeks
    :return:
    """
    updated_info = False
    
    olderthanfourmonths = datetime.utcnow() - (timedelta(weeks=3))


    getmsgs = db.session\
        .query(Service_WebsiteFeedback)\
        .filter(Service_WebsiteFeedback.timestamp < olderthanfourmonths)\
        .all()
    for f in getmsgs:
        db.session.delete(f)
        updated_info = True

    if updated_info is True:
        db.session.commit()
        print("Updated ")
    else:
        print("No work done")


