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


@app.route('/status', methods=['GET'])
def get_daemon_status():
    """
    Gets the count of vendor order issues.  Notification bar at top
    :return:
    """

    return jsonify({
        "status": 'Ready to get coin prices',
    })

@app.route('/orders', methods=['GET'])
def check_orders():
    """
    Checks orders
    :return:
    """
    orders()
    
    return jsonify({
        "status": 'Checking Orders',
    })
    
@app.route('/deletemsgs', methods=['GET'])
def check_old_msgs():
    """
    Delets old msgs
    :return:
    """
    deleteoldmsgs()
    
    return jsonify({
        "status": 'Checked old msgs',
    })
    
    
@app.route('/checkitems', methods=['GET'])
def check_items():
    """
    Checks Items
    :return:
    """
    checkitems()
    
    return jsonify({
        "status": 'Checked Items',
    })
    
@app.route('/checkrating', methods=['GET'])
def check_item_rating():
    """ 
    Checks ratings of items
    :return:
    """
    itemrating()
    
    return jsonify({
        "status": 'Checked item rating',
    })
    
    
    
@app.route('/checkuserstats', methods=['GET'])
def check_user_stats():
    """ 
    Checks user stats
    :return:
    """
    userstats()
    
    return jsonify({
        "status": 'Checked user stats',
    })
    
@app.route('/checkvendorstats', methods=['GET'])
def check_vendor_stats():
    """ 
    Checks user stats
    :return:
    """
    vendorstats()
    
    return jsonify({
        "status": 'Checked vendor stats',
    })
    
@app.route('/checkvendoraway', methods=['GET'])
def check_vendor_away():
    """ 
    Checks if vendor hasnt loggewd in for a
    while and turns off listings
    :return:
    """
    turnoffitems()
    
    return jsonify({
        "status": 'Checked vendor stats',
    })
    