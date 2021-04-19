from app import db
from app.classes.message import Notifications

#1 = sale
#2 = message
#3 = Feedback
#4 = dispute
#5 = return
#6 = bitcoin credit
#7 = Cancelled Order
#8 = succesful return
#9- sold out of item
#55 - return vendor added rreturn label

#10 = Digital Trade
#11 = Cancelled Digital Trade
#12 = Success Digital Trade
#13 = Dispute Digital Trade


#15 = BTC Trade
#16 = Cancelled BTC Trade
#17 = Success BTC Trade
#18 = Dispute BTC Trade

##cron errors
#30 - incorrect address
#30 - incorrect amount(to high or low)

def notification(type, username, userid, salenumber, bitcoin):

    addnotice = Notifications(
                            type = type,
                            username = username,
                            userid = userid,
                            salenumber=salenumber,
                            bitcoin=bitcoin,
                            read = 1,
                             )
    db.session.add(addnotice)
    db.session.commit()
