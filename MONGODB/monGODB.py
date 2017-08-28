from pymongo import MongoClient

from neo4jgraph import GraphClass


def createdb():
    client = MongoClient()
    db = client.Recom
    collection_LO = db.LO
    collection_student_LO = db.Student_LO
    collection_student_Table = db.Student

    collection_student_Table.insert({"name":"shaam", "_id":2, "username": "shaam", "password":"123"})
    collection_student_Table.insert({"name": "gaurav", "_id": 3, "username": "grv", "password": "123"})
    collection_student_Table.insert({"name": "ravi", "_id": 4, "username": "ravi", "password": "123"})
    collection_student_Table.insert({"name": "romi", "_id": 5, "username": "romi", "password": "123"})
    LO1 = {"name": "Introduction to Machine learning", "_id": 1}
    LO2 = {"name": "Supervised Vs Unsupervised", "_id": 2}
    LO3 = {"name": "Linear Regression", "_id": 3}
    LO4 = {"name": "Principle Component Analysis", "_id": 4}
    LO5 = {"name": "K-Means Clustering", "_id": 5}
    LO6 = {"name": "Graphical Model", "_id": 6}
    LO7 = {"name": "Bayes Decision Theory", "_id": 7}
    LO8 = {"name": "Neural Network", "_id": 8}
    LO9 = {"name": "Support Vector Machine ", "_id": 9}
    collection_LO.insert(LO1)
    collection_LO.insert(LO2)
    collection_LO.insert(LO3)
    collection_LO.insert(LO4)
    collection_LO.insert(LO5)
    collection_LO.insert(LO6)
    collection_LO.insert(LO7)
    collection_LO.insert(LO8)
    collection_LO.insert(LO9)

    collection_student_LO.insert({"collection_student_Table_id": 2, "LO": [{"collection_LO_id": 5, "timestamp": "t3", "review": "open"},
                                                                 {"collection_LO_id": 1, "review": "open","timestamp": "t4"},
                                                                {"collection_LO_id": 3, "review": "like","timestamp": "t4"}   ]});

    collection_student_LO.insert({"collection_student_Table_id": 3, "LO": [{"collection_LO_id": 2, "timestamp": "t3", "review": "open"},
                                                                  {"collection_LO_id": 1, "review": "open",
                                                                   "timestamp": "t4"}]});

    collection_student_LO.insert({"collection_student_Table_id": 4, "LO": [{"collection_LO_id": 3, "timestamp": "t3", "review": "open"},
                                                                {"collection_LO_id": 5, "review": "open", "timestamp": "t4"}]});

    collection_student_LO.insert({"collection_student_Table_id": 5, "LO": [{"collection_LO_id": 4 ,"timestamp": "t3", "review": "open"},
                                                                {"collection_LO_id": 4, "review": "open", "timestamp": "t4"},
                                                                {"collection_LO_id": 1, "review": "open", "timestamp": "t4"}]});


def createneo4jdb():
    graph = GraphClass()
    graph.relationship(startnode=graph.InsertStudentNode("grv"),
                       endnode=graph.InsertSubjectNode("Introduction to Machine learning"), review="open")
    graph.relationship(startnode=graph.InsertStudentNode("raam"),
                       endnode=graph.InsertSubjectNode("Introduction to Machine learning"), review="like")
    graph.relationship(startnode=graph.InsertStudentNode("shaam"), endnode=graph.InsertSubjectNode("Linear Regression"),
                       review="like")
    graph.relationship(startnode=graph.InsertStudentNode("ravi"), endnode=graph.InsertSubjectNode("Linear Regression"),
                       review="open")
    graph.relationship(startnode=graph.InsertStudentNode("romi"),
                       endnode=graph.InsertSubjectNode("Principle Component Analysis"), review="like")
    graph.relationship(startnode=graph.InsertStudentNode("romi"),
                       endnode=graph.InsertSubjectNode("Principle Component Analysis"), review="like")
    graph.relationship(startnode=graph.InsertStudentNode("romi"),
                       endnode=graph.InsertSubjectNode("Introduction to Machine learning"), review="like")
    graph.relationship(startnode=graph.InsertStudentNode("grv"),
                       endnode=graph.InsertSubjectNode("Supervised Vs Unsupervised"), review="open")
    graph.relationship(startnode=graph.InsertStudentNode("ravi"),
                       endnode=graph.InsertSubjectNode("K-Means Clustering"), review="open")

    graph.relationship(startnode=graph.InsertStudentNode("shaam"),
                       endnode=graph.InsertSubjectNode("Introduction to Machine learning"), review="open")

    graph.relationship(startnode=graph.InsertStudentNode("shaam"),
                       endnode=graph.InsertSubjectNode("K-Means Clustering"), review="open")


   

if __name__ =='__main__':
    #createdb()
    createneo4jdb()

