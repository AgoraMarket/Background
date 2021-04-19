from app import db
from app.classes.item import marketItem
from app.classes.wallet_bch import BchWallet
from decimal import Decimal

from app.common.functions import \
    btc_cash_convertlocaltobtc
from app.wallet_btccash.wallet_btccash_work import btc_cash_sendCoin_forad
from datetime import datetime


def chargedailyads():
    now = datetime.utcnow()
    getallmarketitems = db.session.query(marketItem).filter(marketItem.aditem == 1).all()
    dollar = btc_cash_convertlocaltobtc(amount=1, currency=1)
    tendollars = btc_cash_convertlocaltobtc(amount=10, currency=1)

    decimaldollar = Decimal(dollar)
    decimaltendollar = Decimal(tendollars)
    for ad in getallmarketitems:
        userwallet = db.session.query(BchWallet).filter_by(userid=ad.vendor_id).first()
        useramount = userwallet.currentbalance

        if ad.aditem_level == 1:
            if useramount > decimaldollar:
                btc_cash_sendCoin_forad(amount=dollar,
                                          comment=ad.id,
                                          userid=ad.vendor_id
                                          )
            else:
                ad.aditem = 0
                ad.aditem_level = 0
                ad.aditem_timer = now

                db.session.add(ad)

        elif ad.aditem_level == 2:
            if useramount > decimaltendollar:
                btc_cash_sendCoin_forad(amount=dollar,
                                          comment=ad.id,
                                          userid=ad.vendor_id
                                          )
            else:
                ad.aditem = 0
                ad.aditem_level = 0
                ad.aditem_timer = now

                db.session.add(ad)

    db.session.commit()


chargedailyads()
