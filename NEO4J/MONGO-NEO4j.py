from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from py2neo import Graph, Node, Relationship
from flask import Flask, jsonify, render_template, request, json
from flask import abort
graph = Graph("http://localhost:7474/db/data/")
db = GraphDatabase("http://localhost:7474/db/data/")

app = Flask(__name__)
def InsertStudentNode(name):
    try:
        Student_node = graph.find_one(label="Student", property_key="name", property_value=name)
        if Student_node is None:
            tx = graph.begin()
            student_n = Node("Student", name=name)
            tx.create(student_n)
            tx.commit()
            return student_n
        else:
            return Student_node
    except :
        print("problem")
        tx.rollback()

def InsertSubjectNode(name):

    try:
        Subject_node = graph.find_one(label="Subject", property_key="name", property_value= name)
        if Subject_node is None:
            tx = graph.begin()
            Subject_n = Node("Subject", name=name)
            tx.create(Subject_n)
            tx.commit()
            return Subject_n
        else:
            return Subject_node
    except :
        print("problem")
        tx.rollback()


def relationship(startnode, endnode, review):
    try:

        tx = graph.begin()
        ab = Relationship(startnode, review, endnode)
        tx.create(ab)
        tx.commit()
    except:
        print("problem")
        tx.rollback()

def Toptrending():
    TopList = []
    RecordList = db.query("MATCH (n)-[r]->(m) RETURN m, COUNT(r) ORDER BY COUNT(r) DESC LIMIT 4 ", returns=(dict,str))
    for record in RecordList:
        TopList.append(record[0]['data']['name'])
    return TopList

def ColabFiltering(user):
    SubjList = []
    RecordList = db.query("MATCH (s:Student)-[:like]->(n:Subject)<-[:like]-()-[:like]->(m:Subject) WHERE s.name = {username} AND  NOT  (s)-[:like]->(m:Subject) RETURN m.name"
                          , params={"username":user},returns=(str))
    for record in RecordList:
        if record[0] not in SubjList:
         SubjList.append(record[0])

    return SubjList






@app.route('/recommendation/neo4j/<string:user>', methods=['GET'])
def recommendation(user):
    dict_recom = {}
    dict_recom['Top Trending'] = Toptrending()
    dict_recom['NeoRecom'] = ColabFiltering(user)

    return jsonify(dict_recom)

@app.route("/tutorial")
def main():
    return render_template('tutorial.html')

@app.route('/showSignUp', methods=['POST'])
def showSignUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html': '<span>All fields good !!</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})
    return render_template('signup.html')


if __name__ =='__main__':

    app.run(debug=True)

    #relationship(startnode=InsertStudentNode("Gaurav"),endnode=InsertSubjectNode("subject-3"),review="like")
    relationship(startnode=InsertStudentNode("raam"), endnode=InsertSubjectNode("subject-5"), review="like")
    relationship(startnode=InsertStudentNode("shaam"), endnode=InsertSubjectNode("subject-2"), review="like")
    relationship(startnode=InsertStudentNode("ravi"), endnode=InsertSubjectNode("subject-6"), review="open")
    relationship(startnode=InsertStudentNode("romi"), endnode=InsertSubjectNode("subject-6"), review="like")
   #relationship(startnode=InsertStudentNode("Gaurav"), endnode=InsertSubjectNode("subject-5"), review="like")



