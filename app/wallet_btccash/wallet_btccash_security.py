from app import db
from app.wallet_btccash.models import btccash_Wallet
from decimal import Decimal


def checkbalance_btccash(userid, amount):
    # The money requested during the trade
    userwallet = db.session.query(btccash_Wallet).filter_by(userid=userid).first()
    theusersbalance = userwallet.currentbalance
    theamountrequested = Decimal(amount)

    if theusersbalance >= theamountrequested:
        return 1
    else:
        return 0
