from app import db
from app.classes.item import Item_MarketItem
from app.classes.wallet_bch import Bch_Wallet
from decimal import Decimal
from app.common.functions import convert_local_to_bch
from app.wallet_bch.wallet_bch_work import bch_send_coin_for_ad
from datetime import datetime



def chargedailyads():
    now = datetime.utcnow()
    getallmarketitems = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.aditem == 1)\
        .all()
    dollar = convert_local_to_bch(amount=1, currency=1)
    tendollars = convert_local_to_bch(amount=10, currency=1)

    decimaldollar = Decimal(dollar)
    decimaltendollar = Decimal(tendollars)


    for ad in getallmarketitems:
        userwallet = db.session.query(Bch_Wallet).filter_by(user_id=ad.vendor_id).first()
        useramount = userwallet.currentbalance

        if ad.aditem_level == 1:
            if useramount > decimaldollar:
                bch_send_coin_for_ad(amount=dollar,
                                      comment=ad.id,
                                      user_id=ad.vendor_id
                                      )
            else:
                ad.aditem = 0
                ad.aditem_level = 0
                ad.aditem_timer = now

                db.session.add(ad)

        elif ad.aditem_level == 2:
            if useramount > decimaltendollar:
                bch_send_coin_for_ad(amount=dollar,
                                      comment=ad.id,
                                      user_id=ad.vendor_id
                                      )
            else:
                ad.aditem = 0
                ad.aditem_level = 0
                ad.aditem_timer = now

                db.session.add(ad)

    db.session.commit()


chargedailyads()
