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

# find similar artworks 
@app.route('/map_get', methods=['GET'])
def get_map_data():
	current_time = ""
	if not current_time:
		timestamp = "2015-09-28" # for testing
	else:
		timestamp = current_time
		
	stmt = "SELECT * FROM art_geo_count WHERE event_time = %s"
		# event_time | code | count | location
	response = cs_session.execute(stmt, parameters=[timestamp])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"code": x.code, "name": x.location, "value": x.count} for x in response_list]
	# return render_template("map.html",output=jsonresponse)
	return jsonify(output=jsonresponse)


# find similar artworks
@app.route('/similar', methods=['POST'])
def img_similar_post():
	req = request.form['artwork_id'] #sim test: 538f6428c9dc24d3d700052c
	art_id = ""
	if not req:
		art_id = "538f6428c9dc24d3d700052c"		
	stmt_2 = "SELECT * FROM artwork_sim WHERE id_1 in %s"
	response_2 = cs_session.execute(stmt_2, parameters=[art_id])
	response_list_2 = []
	for val in response_2:
		response_list_2.append(val)
	jsonresponse_2 = [{"art_id": x.id_1, "similary": x.id_2, "pin_count": x.sim_count} for x in response_list_2]
	return render_template("imgtrenddisplay.html",output=jsonresponse_2)


@app.route("/trend")
def img_trend():
   return render_template("imgtrend.html")

# get image info
@app.route('/trend/<req>', methods=['GET'])
def img_trend_get(req):
	# req = request.form['artwork_id'] #test: 538f6428c9dc24d3d700052c
	art_id = req
	if not art_id:
		art_id = "538f6428c9dc24d3d700052c"

	## Get art info
	stmt_0 = "SELECT artwork_id,image_link, title, collecting_institution, pined_count, sold FROM artworks WHERE artwork_id = %s"
	response_0 = cs_session.execute(stmt_0, parameters=[art_id])
	response_list_0 = []
	for val in response_0:
		response_list_0.append(val)
	jsonresponse_0 = [{"id":x.artwork_id , "title": x.title,"image_link":x.image_link ,"collecting_institution": x.collecting_institution, "pined_count": x.pined_count, "sold":x.sold} for x in response_list_0]

	## Get the trend
	current_time = gmtime()
	to_date = strftime("%Y-%m-%d %H:%M:%S", current_time)
	stmt = "SELECT art_id, pin_count, event_time FROM artwork_count WHERE art_id = %s AND event_time < %s ORDER BY event_time DESC LIMIT 20 ALLOW FILTERING"
	response = cs_session.execute(stmt, parameters=[art_id, to_date])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"art_id": x.art_id, "event_time": x.event_time, "pin_count": x.pin_count} for x in response_list]

	## Get the similar Art too
	stmt_2 = "SELECT * FROM artwork_sim WHERE id_1 in (%s)"
	response_2 = cs_session.execute(stmt_2, parameters=[art_id])
	response_list_2 = []
	jsonresponse_2 = []
	if response_2:
		for val in response_2:
			temp_stmt = "SELECT artwork_id,image_link FROM artworks WHERE artwork_id = %s"
			temp_response = cs_session.execute(temp_stmt, parameters=[val.id_2])
			jsonresponse_2.append({"art_id": temp_response[0].artwork_id, "image_link": temp_response[0].image_link, "pin_count": val.sim_count})
	## End of similar Art

	## Get some art
	stmt_3 = "SELECT artwork_id,image_link,pined_count FROM artworks LIMIT 5 ALLOW FILTERING"
	response_3 = cs_session.execute(stmt_3)
	jsonresponse_3 = []
	if response_3:
		for val in response_3:
			jsonresponse_3.append({"art_id": val.artwork_id, "image_link": val.image_link, "pin_count": val.pined_count})

	return render_template("imgtrenddisplay.html",output_0=jsonresponse_0, output=jsonresponse,output_2=jsonresponse_2,output_3=jsonresponse_3)


# given date, view art's pinned_count
@app.route('/cs/<art_id>') #test: 515b683f94714cb2e3000131
def get_count(art_id):
	current_time = gmtime()
	to_date = strftime("%Y-%m-%d %H:%M:%S", current_time)
	stmt = "SELECT art_id, pin_count,event_time FROM artwork_count WHERE art_id = %s AND event_time < %s ORDER BY event_time DESC LIMIT 5 ALLOW FILTERING"
	response = cs_session.execute(stmt, parameters=[art_id,to_date])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"art_id": x.art_id, "event_time": x.event_time, "pin_count": x.pin_count} for x in response_list]
	return jsonify(output=jsonresponse)

# given date, view art's pinned_count
@app.route('/cs/<art_id>/<from_date>/<to_date>') #works: 515b683f94714cb2e3000131/2015-09-25T02:01:30+0000/2015-09-25T02:04:00+0000
def get_timed_count(art_id, from_date, to_date):
	stmt = "SELECT art_id, pin_count,event_time FROM artwork_count WHERE art_id = %s AND event_time > %s AND event_time < %s"
	response = cs_session.execute(stmt, parameters=[art_id, from_date, to_date])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"Art ID": x.art_id, "Event Time": x.event_time, "Count": x.pin_count} for x in response_list]
	return jsonify(art_id=jsonresponse)


@app.route("/search")
def search():
	return render_template("imgsearch.html")

# search keywords in image title
@app.route('/search', methods=['POST'])
def img_name_post():
	keywords = request.form['keywords']
	if not keywords:
		keywords = "water"
	res = es.search(index = INDEX_NAME, q='title:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	jsonresponse = [{"artwork_id": p[0], "title": p[1], "collecting_institution": p[3], "pinned_count": int(p[4]), "image_link": p[2]} for p in pids]
	return render_template("imgdisply.html",output=jsonresponse)

# search keywords in image title
@app.route('/collection')
def collection_dis():
	keywords = "sunrise"
	res = es.search(index = INDEX_NAME, q='title:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	jsonresponse = [{"artwork_id": p[0], "title": p[1], "collecting_institution": p[3], "pinned_count": int(p[4]), "image_link": p[2]} for p in pids]

	keywords_2 = "sunset"
	res_2 = es.search(index = INDEX_NAME, q='title:'+keywords_2, body={"query": {"match_all": {}}}) 
	pids_2 = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res_2['hits']['hits']]
	pids_2.sort(reverse=True)
	jsonresponse_2 = [{"artwork_id": p[0], "title": p[1], "collecting_institution": p[3], "pinned_count": int(p[4]), "image_link": p[2]} for p in pids_2]
	return render_template("collection.html",output=jsonresponse,output_2=jsonresponse_2)

# given a keyword, return all matches
@app.route('/es/title/<keywords>')
def return_name(keywords):
	res = es.search(index = INDEX_NAME, q={"match_phrase": {"title": keywords}}, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	matched_pics = {}
	count = 0

	for p in pids:
		matched_pics['%04d'%count] = {
			"artwork_id": p[0],
			"title": p[1],
			"collecting_institution": p[3],
			"pinned_count": int(p[4]),
			"Image_link": p[2]
		}
		count += 1
	return json.dumps(matched_pics, indent=2)

# return top 20 in the database for view
@app.route('/es/all/')
def return_all():
	res = es.search(index = INDEX_NAME, size = 50, body={"query": {"match_all": {}}})
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	matched_pics = {}
	count = 0

	for p in pids:
		matched_pics['%04d'%count] = {
			"artwork_id": p[0],
			"title": p[1],
			"collecting_institution": p[3],
			"pinned_count": int(p[4]),
			"Image_link": p[2]
		}
		count += 1
	return json.dumps(matched_pics, indent=2)


if __name__ == '__main__':
	"Are we in the __main__ scope? Start test server."
	app.run(host='0.0.0.0',port=5000,debug=True)