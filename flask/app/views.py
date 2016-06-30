from flask import jsonify
from app import app
from cassandra.cluster import Cluster
from flask import render_template, request
import hashlib
from struct import *
import json
from time import gmtime, strftime
import pytz

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'artsy'
TYPE_NAME = 'artworks'
ID_FIELD = 'id'

#cs_cluster = Cluster(['172.31.11.233','172.31.11.231','172.31.11.232'])
#cs_session = cs_cluster.connect('art_pin_log')
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

#@app.route("/map")  
#def get_map():
#   title = "JustBid"
#   return render_template("map.html", title = title)


# show real-time bids
@app.route('/api/<item_id>/<n>')
def home_page(item_id, n):
    bid_fmt = "%a %b %d %H:%M:%S %Z %Y"
    my_fmt = "%a %b %d %H:%M:%S"
    utc = pytz.timezone('UTC')
    local = pytz.timezone('America/New_York')
    query_for_bids = "SELECT user_id,bid_price from bidding2 WHERE item_id=%d ORDER BY user_id DESC LIMIT 2"
    query_for_name = "SELECT user_id FROM bidding2 WHERE item_id=%d ORDER BY user_id DESC LIMIT 2"
    item_response = session.execute(query_for_name % int(item_id))
    username = "Sidi Chang"
    numOfBid = int(n)
    bid_response = session.execute(query_for_bids % (int(item_id)))
    bids_list = []
    for val in bid_response:
        bids_list.append(val)
        jsonresponse = [{ "Winner": bid.user_id, "Price": bid.bid_price} for bid in bids_list]
    user = {'item_id' : item_id, 'numOfBid' : numOfBid}
    return jsonify(bids=jsonresponse)
'''
    if bid_response:
        return render_template("home_page.html", tweets=json_response, user=user, mode='home')
    else:
        return render_template("home_page.html", user=user, mode='home')
'''
'''
  if uname_response:
    username = uname_response[0].uname
  numOfBid = int(n)
  bid_response = session.execute(query_for_bids % (int(item_id), numOfBid))
  tweet_list = []
  for val in tid_response:
    tweets_response = session.execute(query_for_tweets % int(val.tid))
    for x in tweets_response:
      tweet_list.append(x.tweet)
  json_response = []
  for x in tweet_list:
    tweet_json = json.loads(x, object_pairs_hook=OrderedDict)
    localized_time = utc.localize(datetime.strptime(tweet_json.get('created_at').replace('+0000', 'UTC'), twitter_fmt), is_dst=None).astimezone(local).strftime(my_fmt)
    tweet_simple = {'timestamp' : localized_time, 'text' : tweet_json.get('text'), 'authorName' : tweet_json.get('user').get('name'), 'authorScreenName' : tweet_json.get('user').get('screen_name')}
    hashtags = tweet_json.get('entities').get('hashtags')
    if hashtags:
      hashtag_str = []
      for hashtag in hashtags:
        hashtag_str.append(hashtag.get('text'))
      tweet_simple['hashtags'] = ", ".join(hashtag_str)
    json_response.append(tweet_simple)
  user = {'uid' : uid, 'uname' : username, 'numOfTweet' : numOfTweet}
  if json_response:
    return render_template("home_page.html", tweets=json_response, user=user, mode='home')
  else:
    return render_template("home_page.html", user=user, mode='home')
'''

