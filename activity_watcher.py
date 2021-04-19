from app import db
from app import app
from sendmsg import send_email
from app.classes.message import PostUser


useremail = 'eddwinn@gmail.com'


def findnewmessages():
    getnewmessages = db.session.query(PostUser).count()
    if getnewmessages > 0:
        getlastpost = db.session.query(PostUser).order_by(PostUser.id.asc()).all()
        for newpost in getlastpost:
            with app.app_context():
                postmsg = 'There is a new message: ' + str(newpost.usermsg)
                send_email('Protosbay- New message', [useremail], '',postmsg)


findnewmessages()
