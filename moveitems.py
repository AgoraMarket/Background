from app import db


from app.classes.item import marketItem


def moveitems():
    getitemswithid = db.session.query(marketItem).filter_by(vendor_id=4).all()
    for f in getitemswithid:
        f.online = 1
        f.username = 'dataman'
        f.vendor_id = 22
        db.session.add(f)
    db.session.commit()

moveitems()
