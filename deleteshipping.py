from app import db
from app.classes.vendor import Vendor_Orders
from app.classes.service import Service_ShippingSecret, Service_Tracking
import datetime


# this script run once daily

def deleteshipping():

    """
    # this function ensures shipping is deleted
    :return:
    """

    aweek = datetime.datetime.utcnow() - (datetime.timedelta(weeks=1))
    acceptedorders = db.session.query(Vendor_Orders)
    acceptedorders = acceptedorders.filter(Vendor_Orders.completed == 1,
                                           Vendor_Orders.age < aweek,
                                           Vendor_Orders.released == 1
                                           )
    aorders = acceptedorders.all()
    for specificorder in aorders:
        msg = db.session.query(Service_ShippingSecret).filter_by(orderid=specificorder.id).first()
        gettracking = db.session.query(Service_Tracking).filter_by(sale_id=specificorder.id).first()
        db.session.delete(msg)
        db.session.delete(gettracking)
    db.session.commit()


deleteshipping()

