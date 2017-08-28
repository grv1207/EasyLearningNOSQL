from pymongo import MongoClient
import pandas as pd







def GetData(cursor):
    verb1 = "http://adlnet.gov/expapi/verbs/initialized"
    verb2 = "http://adlnet.gov/expapi/verbs/answered"
    emailID = 'student'
    studentList, LO, accesstime = [], [], []
    for i, document in enumerate(cursor):
        if ((document['statement']['verb']['id'] == verb1 or document['statement']['verb']['id'] == verb2)
            and (document['statement']['object']['definition'])):
            try:
                if ((emailID in document['statement']['actor'].get('name')) and
                        (document['statement']['actor'].get('name') != 'student_01@example.org')) :
                    LO.append(str(document['statement']['object']['definition']['name']['de-DE']))
                    studentList.append(str(document['statement']['actor']['name']))
                    accesstime.append(document['statement']['timestamp'])


            except Exception as e:
                print(document['statement']['object'])
    df_student_LO = pd.DataFrame({'studentID': studentList, 'LOName': LO, 'AccessTime': accesstime})
    df_student_LO.shape
    df_student_LO.to_csv('df_student_LO.csv', index=False)


if __name__ =='__main__':
    client = MongoClient()
    db = client.recommendation
    cursor = db.student.find()
    #GetData(cursor)
    df = pd.read_csv('df_student_LO.csv')
    print(df.shape)