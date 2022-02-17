from app import db
from app.classes.profile import Profile_Exptable
from datetime import datetime
from datetime import timedelta

# run once a day


def deleteoldexp():
    """
    delete all btc trades and chat after 4 weeks
    :return:
    """

    olderthanfourweeks = datetime.utcnow() - (timedelta(weeks=25))
    getexp = db.session.query(Profile_Exptable)
    getexp = getexp.filter(Profile_Exptable.timestamp < olderthanfourweeks)
    getallexp = getexp.all()

    for f in getallexp:
        db.session.delete(f)
    db.session.commit()


deleteoldexp()

