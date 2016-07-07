from flask import jsonify
from app import app
from cassandra.cluster import Cluster
from flask import render_template, request
import hashlib
from struct import *
import json
from time import gmtime, strftime
import pytz

ID_FIELD = 'id'

cluster = Cluster(['ec2-52-204-162-4.compute-1.amazonaws.com'])	
session = cluster.connect('justbid')
# Change tabs
@app.route("/")
@app.route("/index")  
def index():
   title = "JustBid"
   return render_template("home.html", title = title)

@app.route("/profile")  
def profile():
   title = "JustBid"
   return render_template("profile.html", title = title)

@app.route("/slide")  
def get_slide():
   title = "JustBid"
   return render_template("slide.html", title = title)

@app.route("/bidding")
def bidding():
	title = "JustBid"
	return render_template("bidding.html",title= title)

@app.route("/matching")
def matching():
	title = "JustBid"
	return render_template("matching.html",title= title)

#@app.route("/map")  
#def get_map():
#   title = "JustBid"
#   return render_template("map.html", title = title)


# show real-time bids

@app.route('/home_page/<item_id>/<n>')
def home_page(item_id, n):
    bid_fmt = "%a %b %d %H:%M:%S %Z %Y"
    my_fmt = "%a %b %d %H:%M:%S"
    utc = pytz.timezone('UTC')
    local = pytz.timezone('America/New_York')
    #if item_id == 0:
    
    query_for_bids = "SELECT item_id,current_time,user_id,bid_price from bidding3 WHERE item_id =%d LIMIT 10"
    bid_response = session.execute(query_for_bids % int(item_id))
<<<<<<< HEAD
=======
    bids_list = []
    json_response = []
    for val in bid_response:
        bids_list.append(val)
        json_response = [{ "Bidder": bid.user_id, "Current_Time":bid.current_time,"Price": bid.bid_price, "Item":bid.item_id} for bid in bids_list]

    return render_template("home_page.html", bids=json_response)
    
    

# show recommendation
@app.route('/matching_page/<user_id>/<n>')
def matching_page(user_id, n):
    
    query_for_recoms = "SELECT recom_id,MAX(recom_id) from recommendation WHERE user_id=%d"
    user_response = session.execute(query_for_recoms % int(user_id))
    username = "Sidi Chang"
    recom_list = []
    jsonresponse=[]
    numOfRecom = int(n)
    for val in user_response:
        recom_list.append(val)
        jsonresponse = [{"user_ID": user_id, "Matching_user_ID": u.recom_id} for u in recom_list]
    print jsonresponse
    
    recommender_id = jsonresponse[0]["Matching_user_ID"]
    query_for_bids = "SELECT item_id,current_time,user_id,bid_price from bidding_user WHERE user_id =%d LIMIT 30"
    bid_response = session.execute(query_for_bids % int(user_id))
>>>>>>> origin/master
    bids_list = []
    json_response = []
    for val in bid_response:
        bids_list.append(val)
        json_response = [{ "Bidder": bid.user_id, "Current_Time":bid.current_time,"Price": bid.bid_price, "Item":bid.item_id} for bid in bids_list]
<<<<<<< HEAD

    return render_template("home_page.html", bids=json_response)

'''
    else:
        query_for_item = "SELECT item_id,user_id,bid_price FROM bidding3 WHERE item_id=%d LIMIT 1 ALLOW FILTERING"
        item_response = session.execute(query_for_item % int(item_id))
        bids_list = []
        for val in item_response:
            bids_list.append(val)
            json_response = [{ "Bidder": bid.user_id, "Price": bid.bid_price, "Item":bid.item_id} for bid in bids_list]

    username = "Sidi Chang"
    numOfBid = int(n)
 '''   
    
    #user = {'item_id' : item_id, 'numOfBid' : numOfBid}
    #return jsonify(bids=jsonresponse)
    

# show recommendation
@app.route('/matching_page/<user_id>/<n>')
def matching_page(user_id, n):
    
    query_for_recoms = "SELECT recom_id,MAX(recom_id) from recommendation WHERE user_id=%d"
    user_response = session.execute(query_for_recoms % int(user_id))
    username = "Sidi Chang"
    recom_list = []
    jsonresponse=[]
    numOfRecom = int(n)
    #for u in user_response:
     #   recom_id = u.recom_id
    for val in user_response:
        recom_list.append(val)
        jsonresponse = [{"user_ID": user_id, "Matching_user_ID": u.recom_id} for u in recom_list]
    print jsonresponse

    recommender_id = jsonresponse[0]["Matching_user_ID"]
    query_for_bids = "SELECT item_id,current_time,user_id,bid_price from bidding_user WHERE user_id =%d LIMIT 30"
    bid_response = session.execute(query_for_bids % int(user_id))
    bids_list = []
    json_response = []
    for val in bid_response:
        bids_list.append(val)
        json_response = [{ "Bidder": bid.user_id, "Current_Time":bid.current_time,"Price": bid.bid_price, "Item":bid.item_id} for bid in bids_list]
=======
>>>>>>> origin/master
    
    
    
    query_for_us = "SELECT item_id,current_time,user_id,bid_price from bidding_user WHERE user_id =%d LIMIT 30"
    u_response = session.execute(query_for_bids % int(recommender_id))
    us_list = []
    match_response = []
    for val in u_response:
        us_list.append(val)
        match_response = [{ "Bidder": bid.user_id, "Current_Time":bid.current_time,"Price": bid.bid_price, "Item":bid.item_id} for bid in us_list]

<<<<<<< HEAD
    return render_template("matching_page.html", recoms=jsonresponse, bids=json_response, matchs = match_response)#
    
    






=======
    return render_template("matching_page.html", recoms=jsonresponse, bids=json_response, matchs = match_response)
    
>>>>>>> origin/master


if __name__ == '__main__':
	"Are we in the __main__ scope? Start test server."
	app.run(host='0.0.0.0',port=5000,debug=True)

