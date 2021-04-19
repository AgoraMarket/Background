from app import db
from app.classes.vendor import Orders
from app.classes.service import shippingSecret, Tracking
from datetime import \
    datetime,\
    timedelta

# this script run once daily


def deleteshipping():

    """
    # this function ensures shipping is deleted
    :return:
    """

    aweek = datetime.utcnow() - (timedelta(weeks=1))
    acceptedorders = db.session.query(Orders)
    acceptedorders = acceptedorders.filter(Orders.completed == 1,
                                           Orders.age < aweek,
                                           Orders.released == 1
                                           )
    aorders = acceptedorders.all()

    for specificorder in aorders:
        msg = db.session.query(shippingSecret).filter_by(orderid=specificorder.id).first()
        gettracking = db.session.query(Tracking).filter_by(sale_id=specificorder.id).first()
        db.session.delete(msg)
        db.session.delete(gettracking)
    db.session.commit()


deleteshipping()

