from app import db
from datetime import datetime
from app.wallet_btccash.models import TransactionsBtccash


def btc_cash_addtransaction(category, amount, userid, comment, shard, orderid, balance):
    """
    # this function will move the coin from holdings back to vendor.  This is for vendor verification
    :param category:
    :param amount:
    :param userid:
    :param comment:
    :param shard:
    :param orderid:
    :param balance:
    :return:
    """
    try:

        now = datetime.utcnow()
        comment = str(comment)
        orderid = int(orderid)

        trans = TransactionsBtccash(
            category=category,
            userid=userid,
            confirmations=0,
            confirmed=1,
            txid='',
            blockhash='',
            timeoft=0,
            timerecieved=0,
            otheraccount=0,
            address='',
            fee=0,
            created=now,
            commentbtc=comment,
            amount=amount,
            shard=shard,
            orderid=orderid,
            balance=balance,
            digital_currency=3

        )
        db.session.add(trans)
        db.session.commit()

    except Exception as e:
        print("transaction error")
        print(str(e))
