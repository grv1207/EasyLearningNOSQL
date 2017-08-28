from flask import session, jsonify, redirect, url_for, escape, request
from MONGODB import usercheck as uc
from REDIS import RedisSessionInterface
from pymongo import MongoClient

import requests
from flask import Flask, render_template, redirect, url_for, request
from neo4jgraph import GraphClass

#r = redis.StrictRedis(host='localhost')

app = Flask(__name__)
app.session_interface = RedisSessionInterface()




@app.route('/main')
def mainpage():
	print("mainpage")

	return render_template('mainpage.html')

@app.route('/')
def render():
	
    print ("render")

    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])

    return 'You are not logged in, please go to login page at http://127.0.0.1:5000/login'

@app.route('/neo4j/<string:user>', methods=['GET'])
def recommendation(user):


    dict_recom = {}
    graph = GraphClass()
    dict_recom['Top Trending'] = graph.Toptrending()
    dict_recom['NeoRecom'] = graph.ColabFiltering(user)
    
    print ("recommendation")
    return jsonify(dict_recom)



@app.route('/login', methods=['GET','POST'])
def login():


    error = None
    if request.method == 'GET':
        session.pop('username', None)

    if request.method == 'POST':
        session['username'] = request.form['username']
        uid = uc.CheckUser(request.form['username'], request.form['password'])
        if uid != -1:
            return redirect(url_for("mainpage", username=request.form['username'], uid=uid))
        else:
            error = "Wrong username or password, dude"

    return render_template("login.html", error=error)



@app.route('/logout')
def logout():
    # remove the username from the session if it's there

    print("logout")
    session.pop('username', None)
    return redirect(url_for('login'))



@app.route('/signup', methods=['GET','POST'])
def Signup():
    error = None
    print("s1")

    if request.method == 'GET':
    	print("GET CALLED")
    	return render_template("Signup.html")


    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        print(request.form['first'])
        
        if request.form['first'] != '' and request.form['username'] != ''  and request.form['password'] != '':
        	print("going to create user")
        	uc.CreateUser(username=request.form['username'] , password=request.form['password'], name=request.form['first'])
        	return redirect(url_for("login"))
        else:
            error = "Mandatory fields missing"
            return render_template("Signup.html", error=error)


@app.route('/storedata', methods = ['POST'])
def store_student_interactions():
  client = MongoClient()
  db = client.Recom
  data = request.get_json()

  db.Student_LO.update( { "_id" : data["UID"] }, 
  	{ "$push" : { "LO" : { "collection_LO_id" : data["LO_ID"], "timestamp" : data["ts"], "review": data['review']}}},
  	upsert=True)

  graph = GraphClass()
  graph.relationship(startnode=graph.InsertStudentNode(data['username']),
                       endnode=graph.InsertSubjectNode(data["LO_ID"]), review=data['review'])

  return 'OK'


app.secret_key = b'\xe2\x92*\x1b\x96F\xf2\xafh^\xfd\xcf\xde\xb4f\xbd\x0b\xdf\xa1@#\xd4\xb1\x9c'

if __name__ =='__main__':
    app.run(debug=True,use_debugger=True, use_reloader=False)