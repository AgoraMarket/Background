from app import db
from app import errorLogger
from datetime import datetime

from app.wallet_btccash.wallet_btccash_transaction import\
    btc_cash_addtransaction

from app.wallet_btccash.wallet_btccash_security import\
    checkbalance_btccash

# models

from app.auth.models import \
    User

from app.admin.models import \
    Agoraprofit_btccash,\
    Agoraholdings_btccash,\
    AgoraFee

from app.wallet_btccash.models import \
    btccash_Wallet, \
    btccash_Wallet_Work, \
    btccash_walletFee, \
    btccash_walletAddresses,\
    btccash_unconfirmed
# end models

from decimal import Decimal
from app.common.functions import floating_decimals
from app.notification import notification
from app import SHARDBTCCASH

getfees = db.session.query(AgoraFee).filter_by(id=1).first()


def btc_cash_walletstatus(userid):
    """

    THIS function creates the wallet_btc and puts its first address there
    :param userid:
    :return:
    """
    userwallet = db.session.query(btccash_Wallet).filter_by(userid=userid).first()
    getuser = db.session.query(User).filter(User.id == userid).first()
    user = db.session.query(User).filter_by(id=userid).first()
    if userwallet:
        try:
            if userwallet.address1status == 0\
                    and userwallet.address2status == 0\
                    and userwallet.address2status == 0:
                btc_cash_createWallet(userid=userid)

            else:
                pass
            if user.shard_btccash is None:
                user.shard_btccash = SHARDBTCCASH
                db.session.add(user)
                db.session.commit()

            if user.monero_fee is None:
                user.btc_cash_fee = getfees.btc_cash_trade
                db.session.add(user)
                db.session.commit()

            if user.btc_cash_fee_enddate is None:
                user.btc_cash_fee_enddate = datetime.utcnow()
                db.session.add(user)
                db.session.commit()

        except Exception as e:
            print(str(e))
            userwallet.address1 = ''
            userwallet.address1status = 0
            userwallet.address2 = ''
            userwallet.address2status = 0
            userwallet.address3 = ''
            userwallet.address3status = 0

            db.session.add(userwallet)
            db.session.commit()
            btc_cash_createWallet(userid == userid)
    else:
        # creates wallet_btc in db
        walletcreate = btccash_Wallet(userid=userid,
                                      currentbalance=0,
                                      unconfirmed=0,
                                      address1='',
                                      address1status=0,
                                      address2='',
                                      address2status=0,
                                      address3='',
                                      address3status=0,
                                      locked=0,
                                      shard=getuser.shard_btccash,
                                      transactioncount=0
                                      )

        db.session.add(walletcreate)
        db.session.commit()

# THIS function creates the wallet_btc and puts its first address there


def btc_cash_createWallet(userid):
    try:
        userswallet = db.session.query(btccash_Wallet) \
            .filter_by(userid=userid).first()
        if userswallet:
            x = db.session.query(btccash_walletAddresses)\
                .filter(btccash_walletAddresses.status == 0,
                        btccash_walletAddresses.shard == userswallet.shard).first()

            userswallet.address1 = x.btcaddress
            userswallet.address1status = 1

            x.shard = SHARDBTCCASH
            x.userid = userid
            x.status = 1
            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()
        else:
            btc_cash_walletcreate = btccash_Wallet(userid=userid,
                                                   currentbalance=0,
                                                   unconfirmed=0,
                                                   address1='',
                                                   address1status=0,
                                                   address2='',
                                                   address2status=0,
                                                   address3='',
                                                   address3status=0,
                                                   locked=0,
                                                   shard=SHARDBTCCASH,
                                                   transactioncount=0
                                                   )
            btc_cash_newunconfirmed = btccash_unconfirmed(
                userid=userid,
                unconfirmed1=0,
                unconfirmed2=0,
                unconfirmed3=0,
                unconfirmed4=0,
                unconfirmed5=0,
                unconfirmed6=0,
                unconfirmed7=0,
                unconfirmed8=0,
                unconfirmed9=0,
                unconfirmed10=0,
            )
            db.session.add(btc_cash_walletcreate)
            db.session.add(btc_cash_newunconfirmed)
            db.session.commit()

            x = db.session.query(btccash_walletAddresses) \
                .filter(btccash_walletAddresses.status == 0,
                        btccash_walletAddresses.shard == userswallet.shard).first()

            userswallet.address1 = x.btcaddress
            userswallet.address1status = 1

            x.shard = SHARDBTCCASH
            x.userid = userid
            x.status = 1
            db.session.add(userswallet)
            db.session.add(x)
            db.session.commit()

    except Exception as e:
        print("btc_cash_createWalle")
        print(str(e))


# OFF SITE
# withdrawl


def btc_cash_sendCoin(userid, sendto, amount, comment):

    getwallet = btccash_walletFee.query.filter_by(id=1).first()
    walletfee = getwallet.btc
    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:

        strcomment = str(comment)
        type_transaction = 2
        timestamp = datetime.utcnow()
        userswallet = btccash_Wallet.query.filter_by(userid=userid).first()

        wallet = btccash_Wallet_Work(
            userid=userid,
            type=type_transaction,
            amount=amount,
            sendto=sendto,
            comment=0,
            created=timestamp,
            txtcomment=strcomment,
            shard=userswallet.shard
        )

        db.session.add(wallet)
        db.session.commit()

        # turn sting to a decimal
        amountdecimal = Decimal(amount)
        # make decimal 8th power
        amounttomod = floating_decimals(amountdecimal, 8)
        # gets current balance
        curbalance = floating_decimals(userswallet.currentbalance, 8)
        # gets amount and fee
        amountandfee = floating_decimals(amounttomod + walletfee, 8)
        # subtracts amount and fee from current balance
        y = floating_decimals(curbalance - amountandfee, 8)
        # set balance as new amount
        userswallet.currentbalance = floating_decimals(y, 8)

        db.session.add(userswallet)
        db.session.commit()


    else:
        notification(
            type=34,
            username='',
            userid=userid,
            salenumber=0,
            bitcoin=amount
        )


# TO Agora Wallet
# this function will move the coin to agoras wallet_btc from a user


def btc_cash_sendCointoEscrow(amount, comment, userid):

    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:
        try:

            type_transaction = 4
            userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
            curbal = Decimal(userswallet.currentbalance)
            amounttomod = Decimal(amount)
            newbalance = Decimal(curbal) - Decimal(amounttomod)
            userswallet.currentbalance = newbalance
            db.session.add(userswallet)
            db.session.commit()
            oid = int(comment)
            btc_cash_addtransaction(category=type_transaction,
                                    amount=amount,
                                    userid=userid,
                                    comment='Sent Coin To Escrow',
                                    shard=userswallet.shard,
                                    orderid=oid,
                                    balance=newbalance
                                    )

        except Exception as e:
            print(str(e))
            notification(
                type=34,
                username='',
                userid=userid,
                salenumber=comment,
                bitcoin=amount
            )
    else:
        print("a equals", a)
        notification(
            type=34,
            username='',
            userid=userid,
            salenumber=comment,
            bitcoin=amount
        )





def btc_cash_sendCointoUser(amount, comment, userid):
    """
    #TO User
    ##this function will move the coin from agoras wallet_btc to a user
    :param amount:
    :param comment:
    :param userid:
    :return:
    """
    try:
        type_transaction = 5
        oid = int(comment)

        userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = Decimal(amount)
        newbalance = Decimal(curbal) + Decimal(amounttomod)
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)
        db.session.commit()

        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=userid,
                                comment='Transaction',
                                shard=userswallet.shard,
                                orderid=oid,
                                balance=newbalance
                                )
    except Exception as e:
        print(str(e))
        print("btc_cash_sendCointoUser")
        errorLogger(function='sendcointouser', error=e, kindoferror=4, user=userid)

        db.session.rollback()

def btc_cash_sendCointoUser_asAdmin(amount, comment, userid):
    """
    #TO User
    ##this function will move the coin from agoras wallet_btc to a user as an admin
    :param amount:
    :param comment:
    :param userid:
    :return:
    """
    try:
        type_transaction = 9

        userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = Decimal(amount)
        newbalance = Decimal(curbal) + Decimal(amounttomod)
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)
        db.session.commit()

        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=userid,
                                comment=comment,
                                shard=userswallet.shard,
                                orderid=0,
                                balance=newbalance
                                )
    except Exception as e:
        print(str(e))
        errorLogger(function='sendcointouser', error=e, kindoferror=4, user=userid)
        db.session.rollback()


def btc_cash_takeCointoUser_asAdmin(amount, comment, userid):
    """
    # TO User
    # this function will move the coin from agoras wallet_btc to a user as an admin
    :param amount:
    :param comment:
    :param userid:
    :return:
    """
    try:
        type_transaction = 10
        a = Decimal(amount)
        userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = Decimal(amount)
        newbalance = Decimal(curbal) - Decimal(amounttomod)
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)
        db.session.commit()

        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=userid,
                                comment=comment,
                                shard=userswallet.shard,
                                orderid=0,
                                balance=newbalance
                                )

        getcurrentprofit = db.session.query(Agoraprofit_btccash).order_by(Agoraprofit_btccash.id.desc()).first()
        currentamount = floating_decimals(getcurrentprofit.total, 8)
        newamount = floating_decimals(currentamount, 8) + floating_decimals(a, 8)
        prof = Agoraprofit_btccash(
            amount=amount,
            timestamp=datetime.utcnow(),
            total=newamount
        )
        db.session.add(prof)
        db.session.commit()

    except Exception as e:
        print(str(e))
        errorLogger(function='sendcointouser', error=e, kindoferror=4, user=userid)
        db.session.rollback()



def btc_cash_sendCointoAgora(amount, comment, shard):
    """
    # TO Agora
    # this function will move the coin from agoras escrow to profit account
    # no balance necessary
    :param amount:
    :param comment:
    :param shard:
    :return:
    """
    try:
        type_transaction = 6
        now = datetime.utcnow()
        oid = int(comment)
        a = Decimal(amount)
        btc_cash_addtransaction(
            category=type_transaction,
            amount=amount,
            userid=1,
            comment='Sent Coin to Agora profit',
            shard=shard,
            orderid=oid,
            balance=0
        )

        getcurrentprofit = db.session.query(Agoraprofit_btccash).order_by(Agoraprofit_btccash.id.desc()).first()
        currentamount = floating_decimals(getcurrentprofit.total, 8)
        newamount = floating_decimals(currentamount, 8) + floating_decimals(a, 8)
        prof = Agoraprofit_btccash(
            amount=amount,
            order=oid,
            timestamp=now,
            total=newamount
        )
        db.session.add(prof)
        db.session.commit()

    except Exception as e:
        print(str(e))
        errorLogger(function='sendcointoagora', error=e, kindoferror=4, user=1)
        db.session.rollback()





def btc_cash_sendCointoHoldings(amount, userid, comment):
    """
    # TO Agora
    # this function will move the coin from vendor to agora holdings.  This is for vendor verification
    :param amount:
    :param userid:
    :param comment:
    :return:
    """
    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:
        try:
            type_transaction = 7
            now = datetime.utcnow()
            user = db.session.query(User).filter(User.id == userid).first()
            userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
            curbal = Decimal(userswallet.currentbalance)
            amounttomod = floating_decimals(amount, 8)
            newbalance = floating_decimals(curbal, 8) - floating_decimals(amounttomod, 8)
            userswallet.currentbalance = newbalance
            db.session.add(userswallet)
            db.session.commit()

            c = str(comment)
            a = Decimal(amount)
            commentstring = "Vendor Verification: Level " + c
            btc_cash_addtransaction(category=type_transaction,
                                    amount=amount,
                                    userid=user.id,
                                    comment=commentstring,
                                    shard=user.shard_btccash,
                                    orderid=0,
                                    balance=newbalance
                                    )

            getcurrentholdings = db.session.query(Agoraholdings_btccash).order_by(Agoraholdings_btccash.id.desc()).first()
            currentamount = floating_decimals(getcurrentholdings.total, 8)
            newamount = floating_decimals(currentamount, 8) + floating_decimals(a, 8)

            holdingsaccount = Agoraholdings_btccash(
                amount=a,
                timestamp=now,
                userid=userid,
                total=newamount
            )

            db.session.add(holdingsaccount)
            db.session.commit()

        except Exception as e:
            print(str(e))
            errorLogger(function='sendcointoholdings', error=e, kindoferror=4, user=userid)
            db.session.rollback()
    else:
        pass


def btc_cash_sendCoinfromHoldings(amount, userid, comment):
    """
    # TO Agora
    # this function will move the coin from holdings back to vendor.  This is for vendor verification
    :param amount:
    :param userid:
    :param comment:
    :return:
    """
    try:
        type_transaction = 8
        now = datetime.utcnow()
        user = db.session.query(User).filter(User.id == userid).first()
        userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = Decimal(amount)
        newbalance = Decimal(curbal) + Decimal(amounttomod)
        userswallet.currentbalance = newbalance

        db.session.add(userswallet)
        db.session.commit()

        c = str(comment)
        a = Decimal(amount)
        commentstring = "Vendor Verification Refund: Level " + c

        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=user.id,
                                comment=commentstring,
                                shard=user.shard_btccash,
                                orderid=0,
                                balance=newbalance
                                )

        getcurrentholdings = db.session.query(Agoraholdings_btccash).order_by(Agoraholdings_btccash.id.desc()).first()
        currentamount = floating_decimals(getcurrentholdings.total, 8)
        newamount = floating_decimals(currentamount, 8) - floating_decimals(a, 8)

        holdingsaccount = Agoraholdings_btccash(
            amount=a,
            timestamp=now,
            userid=userid,
            total=newamount
        )
        db.session.add(holdingsaccount)
        db.session.commit()

    except Exception as e:
        print(str(e))
        errorLogger(function='sendcoinfromholdings', error=e, kindoferror=4, user=userid)
        db.session.rollback()


def btc_cash_sendcointoaffiliate(amount, comment, userid):
    """
    # TO Agora
    # this function will move the coin from agoras escrow to profit account
    # no balance necessary
    :param amount:
    :param comment:
    :param shard:
    :return:
    """
    try:
        type_transaction = 11

        oid = int(comment)

        userswallet = btccash_Wallet.query.filter_by(userid=userid).first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = Decimal(amount)
        newbalance = Decimal(curbal) + Decimal(amounttomod)
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)
        db.session.commit()

        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=userid,
                                comment='Transaction',
                                shard=userswallet.shard,
                                orderid=oid,
                                balance=newbalance
                                )
    except Exception as e:
        print(str(e))
        errorLogger(function='sendcointoagora', error=e, kindoferror=4, user=1)
        db.session.rollback()
