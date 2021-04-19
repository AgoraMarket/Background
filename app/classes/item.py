from app import db


class Categories(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'Agora_Market_Items'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.TEXT)


class ItemtoDelete(db.Model):
    __tablename__ = 'itemtodelete'
    __bind_key__ = 'Agora_Market_Crawler'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    itemid = db.Column(db.Integer)


class ShoppingCart(db.Model):
    __tablename__ = 'shoppingcart'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    customer = db.Column(db.Text)
    customer_id = db.Column(db.INTEGER)
    vendor = db.Column(db.Text)
    vendor_id = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    title_of_item = db.Column(db.Text)
    price_of_item = db.Column(db.DECIMAL(20, 2))
    stringauctionid = db.Column(db.Text)
    stringnodeid = db.Column(db.Text)
    image_of_item = db.Column(db.Text)
    quantity_of_item = db.Column(db.INTEGER)
    return_policy = db.Column(db.Text)
    savedforlater = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    vendorsupply = db.Column(db.INTEGER)
    shippinginfo0 = db.Column(db.Text)
    shippingdayleast0 = db.Column(db.INTEGER)
    shippingdaymost0 = db.Column(db.INTEGER)
    shippinginfo2 = db.Column(db.Text)
    shippingprice2 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast2 = db.Column(db.INTEGER)
    shippingdaymost2 = db.Column(db.INTEGER)
    shippinginfo3 = db.Column(db.Text)
    shippingprice3 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast3 = db.Column(db.INTEGER)
    shippingdaymost3 = db.Column(db.INTEGER)
    shippingfree = db.Column(db.INTEGER)
    shippingtwo = db.Column(db.INTEGER)
    shippingthree = db.Column(db.INTEGER)
    return_allowed = db.Column(db.INTEGER)
    digital_currency1 = db.Column(db.INTEGER)
    digital_currency2 = db.Column(db.INTEGER)
    digital_currency3 = db.Column(db.INTEGER)
    selected_currency = db.Column(db.INTEGER)
    selected_shipping = db.Column(db.INTEGER)
    selected_shipping_description = db.Column(db.Text)
    final_shipping_price = db.Column(db.DECIMAL(20, 8))
    final_price = db.Column(db.DECIMAL(20, 8))


class ShoppingCartTotal(db.Model):
    __tablename__ = 'shoppingcarttotal'
    __bind_key__ = 'Agora_Market'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    customer = db.Column(db.INTEGER)
    btc_sumofitem = db.Column(db.INTEGER)
    btcprice = db.Column(db.DECIMAL(20, 8))
    shippingbtcprice = db.Column(db.DECIMAL(20, 8))
    totalbtcprice = db.Column(db.DECIMAL(20, 8))
    btc_cash_sumofitem = db.Column(db.INTEGER)
    btc_cash_price = db.Column(db.DECIMAL(20, 8))
    shipping_btc_cashprice = db.Column(db.DECIMAL(20, 8))
    total_btc_cash_price = db.Column(db.DECIMAL(20, 8))
    # affiliate stuff
    percent_off_order = db.Column(db.DECIMAL(6, 2))
    btc_cash_off = db.Column(db.DECIMAL(20, 8))
    btc_off = db.Column(db.DECIMAL(20, 8))


class Cats(db.Model):
    __tablename__ = 'cats'
    __bind_key__ = 'Agora_Market_Items'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    catid0 = db.Column(db.INTEGER, db.ForeignKey('marketitem.categoryid0', name="fk_cat5"), nullable=False)
    catname0 = db.Column(db.TEXT)
    formname = db.Column(db.TEXT)


class marketItem(db.Model):
    __tablename__ = 'marketitem'
    __bind_key__ = 'Agora_Market_Items'
    __table_args__ = {'useexisting': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    online = db.Column(db.INTEGER)
    created = db.Column(db.DATETIME)
    price = db.Column(db.DECIMAL(20, 2))
    vendor_name = db.Column(db.Text)
    vendor_id = db.Column(db.INTEGER)
    stringauctionid = db.Column(db.Text)
    stringnodeid = db.Column(db.Text)

    origincountry = db.Column(db.INTEGER)
    destinationcountry = db.Column(db.INTEGER)
    destinationcountrytwo = db.Column(db.INTEGER)
    destinationcountrythree = db.Column(db.INTEGER)
    destinationcountryfour = db.Column(db.INTEGER)
    destinationcountryfive = db.Column(db.INTEGER)

    itemtitlee = db.Column(db.Text)
    itemcount = db.Column(db.INTEGER)
    itemdescription = db.Column(db.Text)
    keywords = db.Column(db.Text)
    itemcondition = db.Column(db.INTEGER)

    itemrefundpolicy = db.Column(db.Text)
    return_allowed = db.Column(db.INTEGER)

    imageone = db.Column(db.Text)
    imagetwo = db.Column(db.Text)
    imagethree = db.Column(db.Text)
    imagefour = db.Column(db.Text)
    imagefive = db.Column(db.Text)


    details = db.Column(db.BOOLEAN)
    details1 = db.Column(db.Text)
    details1answer = db.Column(db.Text)
    details2 = db.Column(db.Text)
    details2answer = db.Column(db.Text)
    details3 = db.Column(db.Text)
    details3answer = db.Column(db.Text)
    details4 = db.Column(db.Text)
    details4answer = db.Column(db.Text)
    details5 = db.Column(db.Text)
    details5answer = db.Column(db.Text)
    details6 = db.Column(db.Text)
    details6answer = db.Column(db.Text)
    details7 = db.Column(db.Text)
    details7answer = db.Column(db.Text)
    details8 = db.Column(db.Text)
    details8answer = db.Column(db.Text)
    details9 = db.Column(db.Text)
    details9answer = db.Column(db.Text)
    details10 = db.Column(db.Text)
    details10answer = db.Column(db.Text)

    viewcount = db.Column(db.INTEGER)
    itemrating = db.Column(db.DECIMAL(20, 2))
    reviewcount = db.Column(db.INTEGER)
    totalsold = db.Column(db.INTEGER)

    shippinginfo0 = db.Column(db.Text)
    shippingdayleast0 = db.Column(db.INTEGER)
    shippingdaymost0 = db.Column(db.INTEGER)
    shippinginfo2 = db.Column(db.Text)
    shippingprice2 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast2 = db.Column(db.INTEGER)
    shippingdaymost2 = db.Column(db.INTEGER)
    shippinginfo3 = db.Column(db.Text)
    shippingprice3 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast3 = db.Column(db.INTEGER)
    shippingdaymost3 = db.Column(db.INTEGER)

    notshipping1 = db.Column(db.INTEGER)
    notshipping2 = db.Column(db.INTEGER)
    notshipping3 = db.Column(db.INTEGER)
    notshipping4 = db.Column(db.INTEGER)
    notshipping5 = db.Column(db.INTEGER)
    notshipping6 = db.Column(db.INTEGER)
    shippingfree = db.Column(db.BOOLEAN)
    shippingtwo = db.Column(db.INTEGER)
    shippingthree = db.Column(db.INTEGER)

    currency = db.Column(db.INTEGER)
    digital_currency1 = db.Column(db.INTEGER)
    digital_currency2 = db.Column(db.INTEGER)
    digital_currency3 = db.Column(db.INTEGER)

    # Protos Item
    amazonid = db.Column(db.TEXT)
    amazon_last_checked = db.Column(db.DateTime)

    # categories
    categoryname0 = db.Column(db.Text)
    categoryid0 = db.Column(db.INTEGER, db.ForeignKey('cats.catid0'))

    aditem = db.Column(db.INTEGER)
    aditem_level = db.Column(db.INTEGER)
    aditem_timer = db.Column(db.DATETIME)

    def __str__(self):
        return 'marketItem %s' % self.id

    def __repr__(self):
        return '<User %r>' % self.username


db.configure_mappers()
db.create_all()
db.session.commit()