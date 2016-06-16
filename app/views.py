from flask import render_template
#from flask import jsonify
from app import app
from cassandra.cluster import Cluster

cluster = Cluster(['ec2-52-87-1-210.compute-1.amazonaws.com'])

session = cluster.connect('playground')

@app.route('/')
@app.route('/index')

def index():
    user = {'nickname': 'Miguel'} # fake user
    return render_template("index.html", title = 'Home', user = user)

#def index():
#  return "Hello, World!"


@app.route('/api/<email>/<date>')
def get_email(email, date):
       stmt = "SELECT * FROM email WHERE id=%s and date=%s"
       response = session.execute(stmt, parameters=[email, date])
       response_list = []
       for val in response:
            response_list.append(val)
       jsonresponse = [{"first name": x.fname, "last name": x.lname, "id": x.id, "message": x.message, "time": x.time} for x in response_list]
       return jsonify(emails=jsonresponse)


