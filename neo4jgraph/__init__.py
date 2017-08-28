from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from py2neo import Graph, Node, Relationship
from flask import Flask, jsonify, render_template, request, json
from flask import abort



class GraphClass():
    dbb= ''
    graph = ''
    def __init__(self):
        self.db = GraphDatabase("http://localhost:7474/db/data/")
        self.graph = Graph("http://localhost:7474/db/data/")

    def InsertStudentNode(self, name):
        try:
            Student_node = self.graph.find_one(label="Student", property_key="name", property_value=name)
            if Student_node is None:
                tx = self.graph.begin()
                student_n = Node("Student", name=name)
                tx.create(student_n)
                tx.commit()
                return student_n
            else:
                return Student_node
        except:
            print("problem with student node insert")
            tx.rollback()

    def InsertSubjectNode(self, name):

        try:
            Subject_node = self.graph.find_one(label="Subject", property_key="name", property_value=name)
            if Subject_node is None:
                tx = self.graph.begin()
                Subject_n = Node("Subject", name=name)
                tx.create(Subject_n)
                tx.commit()
                return Subject_n
            else:
                return Subject_node
        except:
            print("problem with subject node insert")
            tx.rollback()

    def relationship(self, startnode, endnode, review):
        try:

            tx = self.graph.begin()
            ab = Relationship(startnode, review, endnode)
            tx.create(ab)
            tx.commit()
        except:
            print("problem with relationship")
            tx.rollback()

    def Toptrending(self):
        TopList = []
        RecordList = self.db.query("MATCH (n)-[r]->(m) RETURN m, COUNT(r) ORDER BY COUNT(r) DESC LIMIT 4 ",
                                   returns=(dict, str))
        for record in RecordList:
            TopList.append(record[0]['data']['name'])
        return TopList

    def ColabFiltering(self,user):
        SubjList = []
        RecordListLike = self.db.query(
            "MATCH (s:Student)-[:like]->(n:Subject)<-[:like]-()-[:like]->(m:Subject) WHERE s.name = {username} AND  NOT  (s)-[:like]->(m:Subject) RETURN m.name"
            , params={"username": user}, returns=(str))
        RecordListOpen = self.db.query(
            "MATCH (s:Student)-[:open]->(n:Subject)<-[:open]-()-[:open]->(m:Subject) WHERE s.name = {username} AND  NOT  (s)-[:open]->(m:Subject) RETURN m.name"
            , params={"username": user}, returns=(str))

        for record in RecordListLike:
            if record[0] not in SubjList:
                SubjList.append(record[0])

        for record in RecordListOpen:
            if record[0] not in SubjList:
                SubjList.append(record[0])

        return SubjList




#if __name__ == '__main__':
    #app.run(debug=True)
   # graph = GraphClass()
   # print(graph.ColabFiltering(user='grv'))

    """relationship(startnode=InsertStudentNode("raam"), endnode=InsertSubjectNode("subject-5"), review="like")
    relationship(startnode=InsertStudentNode("grv"), endnode=InsertSubjectNode("subject-3"), review="like")
    relationship(startnode=InsertStudentNode("shaam"), endnode=InsertSubjectNode("subject-2"), review="like")
    relationship(startnode=InsertStudentNode("ravi"), endnode=InsertSubjectNode("subject-6"), review="open")
    relationship(startnode=InsertStudentNode("romi"), endnode=InsertSubjectNode("subject-6"), review="like")
    relationship(startnode=InsertStudentNode("grv"), endnode=InsertSubjectNode("subject-5"), review="like") """



