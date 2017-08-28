import operator
import pandas as pd
import numpy as np
from collections import OrderedDict
import time


def weight_matrix(student_id, LO_Count_pivot):
    # LO_Count=pd.read_csv('GroupdData.json')
    """
    Input : Takes arguemnt as each student id and Group data json file(which contains count of LOs for each Student)
    Output:
              Return Wieght_Matrix, which contains weight of each LOs corresponds to respective stduents.
    """
    LO_weight = np.array(LO_Count_pivot.iloc[student_id, :].dropna(axis=0))  # weight corresponding to each student
    return LO_weight


def Similarity_Matrix(pickle_file):
    """
    Input : Takes Pickle file, which is the calculation of Similairity matrix.
    Output: Retrun Similraity matrix corresponding to each LOs.

    """
    pickle1 = pd.read_pickle(pickle_file)
    Utility_data = pd.DataFrame(pickle1)
    a = list(Utility_data)
    Similarity_matrix = pd.DataFrame.from_dict(pickle1, orient='index', dtype=None)
    Similarity_matrix.columns = a
    return Similarity_matrix


def rating_recommendation_with_dict(top_recom, df, LO_Count_file):
    """
    Input : Takes number of items to be recommended, dataframe df of student &LOs and LOs count json file for each student
    Output: Return list of all possible recommendtaions corresponding to each students.

    """

    # LO_Count=pd.read_csv("GroupdData.json")
    LO_Count = pd.read_csv(LO_Count_file)
    LO_list = LO_Count['object.definition.name.de-DE'].unique()
    LO_ID = ['LO_' + str(x) for x in range(len(LO_list))]
    zip(LO_ID, LO_list)
    dict_List = {}
    for k, v in zip(LO_list, LO_ID):
        dict_List[k] = v
    LO_Count['LO'] = LO_Count['object.definition.name.de-DE'].apply(lambda x: dict_List[x])
    LO_Count_pivot = LO_Count.pivot(index='actor.name', columns='LO', values='count')
    # LO_Count_pivot.head()
    ratings = []
    Similarity_matrix = Similarity_Matrix('dictionary.pickle')  # Get similarity matrix for item to item
    rat1 = {}
    ratings1 = []
    for i in range(0, df.shape[0]):  # Loop Till number of Students
        stu_data_index = df.iloc[[i]]  # get each of Student data
        not_done = list(stu_data_index.columns[stu_data_index.isnull().any()])  # Find LOs not done by Student
        done = list(stu_data_index.dropna(axis=1))  # Get LOs done by the student
        rat, list1 = [], []
        rat1 = {}
        for k in range(0, len(not_done)):
            df_weight = weight_matrix(i, LO_Count_pivot)  # Weight matrix for each student
            similarilty_student = np.array(Similarity_matrix.loc[not_done[k], done])
            rat1[(similarilty_student.dot(df_weight.T)) / similarilty_student.sum()] = not_done[k]
            od = OrderedDict(sorted(rat1.items(), reverse=True)[:top_recom])
        ratings1.append(od)
    return ratings1


def recommendation():
    """
    Input :
    Output:  It return list of top-N recommendation
    """
    df= pd.read_csv('df_Student_User')                         #read Student and LOs data corresponding to each in dataframe df
    df.set_index('StudentID',inplace=True)                      #Set index of df as StudentID
    t=time.clock()
    rating_dictionary = rating_recommendation_with_dict(5,df,'GroupdData.json')
    print(time.clock()-t)
    print("rating matrix length= "+str(len(rating_dictionary)))
    rating_dict_final={}
    for i in range(0,len(rating_dictionary)):
        rating_dict_final[df.index[i]]=rating_dictionary[i]       #Stoting top-N recommendation in dict
    return rating_dict_final


if __name__ == '__main__':
    recommendation()