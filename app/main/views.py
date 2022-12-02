from flask import jsonify
from app.scripts import\
    checkitems,\
    deleteoldmsgs,\
    itemrating,\
    orders,\
    turnoffitems,\
    userstats,\
    vendorstats
from app import app


@app.route('/', methods=['GET'])
def get_daemon_status():
    """
    Gets the status of cron job server
    :return:
    """

    return jsonify({
        "status": 'Ready to do background work',
    })

@app.route('/orders', methods=['GET'])
def check_orders():
    """
    Checks orders to see if old, new, needs to be cancelled etc
    :return:
    """
    orders.neworders_48hours()
    orders.acceptedorders_1week()
    orders.requestcancel_24rs()
    orders.autofinalize_20days()
    
    return jsonify({
        "status": 'Checking Orders',
    })

@app.route('/deletemsgs', methods=['GET'])
def check_old_msgs():
    """
    Delets old msgs
    :return:
    """
    deleteoldmsgs.deleteoldfeedback()
    deleteoldmsgs.deleteoldmsgs()
    deleteoldmsgs.deleteoldmcomments()
    deleteoldmsgs.deletesecretshipping()
    deleteoldmsgs.deletereturnsshipping()
    
    return jsonify({
        "status": 'Checked old msgs',
    })
    
    
@app.route('/checkitems', methods=['GET'])
def check_items():
    """
    Checks Items to see if they are bad like no image etc
    :return:
    """
    checkitems.turnoffmarketitems()
    
    return jsonify({
        "status": 'Checked Items',
    })
    
@app.route('/checkrating', methods=['GET'])
def check_item_rating():
    """ 
    Gets ratings of items 
    :return:
    """
    itemrating.marketitemrating()
    
    return jsonify({
        "status": 'Checked item rating',
    })
    
    
    
@app.route('/checkuserstats', methods=['GET'])
def check_user_stats():
    """ 
    Gets user rating and stats
    :return:
    """
    userstats.userrating()
    
    return jsonify({
        "status": 'Checked user stats',
    })
    
@app.route('/checkvendorstats', methods=['GET'])
def check_vendor_stats():
    """ 
    Gets vendor stats
    :return:
    """
    vendorstats.vendorrating()
    
    return jsonify({
        "status": 'Checked vendor stats',
    })
    
@app.route('/checkvendoraway', methods=['GET'])
def check_vendor_away():
    """ 
    Checks if vendor hasnt logged in for a
    while and turns off listings
    :return:
    """
    turnoffitems.main()
    
    return jsonify({
        "status": 'Checked vendor online status',
    })
    