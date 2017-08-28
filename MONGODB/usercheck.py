from pymongo import MongoClient




def CheckUser(username, password):
    client = MongoClient()
    db = client.Recom
    student = db.Student
    sid = -1
    data = student.find_one({"username":username})
    
    if data and password == data['password']:
        paswwd = data['password']
        sid = data["_id"]
    return sid




def CreateUser(username, password, name):
    client = MongoClient()
    db = client.Recom
    collection_student_Table = db.Student

    data = collection_student_Table.insert({"name":name, "username": username, "password":password})
    print(data)