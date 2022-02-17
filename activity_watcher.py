from app import db
from app import app
from sendmsg import send_email
from app.classes.message import Message_PostUser


user_email = 'eddwinn@gmail.com'

def findnewmessages():
    getnewmessages = db.session.query(Message_PostUser).count()
    if getnewmessages > 0:
        getlastpost = db.session.query(Message_PostUser).order_by(Message_PostUser.id.asc()).all()
        for newpost in getlastpost:
            with app.app_context():
                postmsg = 'There is a new message: ' + str(newpost.usermsg)
                send_email('Clearnet- New message', [user_email], '',postmsg)


findnewmessages()
