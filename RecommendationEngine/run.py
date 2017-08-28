import datetime
import logging
import multiprocessing as mp
import pickle
import socket
from functools import partial
from itertools import repeat

import pandas as pd

from RecommendationEngine import functions as fn

def SimilarityMatrix(dataframe):

    """
    Finds the item-item similarity matrix and stores result in a dictionary(dictionary.pickle)
    Input: Dataframe (student-LO matrix)
    Output : Time taken to create the  item-item similarity matrix
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('similaritymatrix')
    logger.info('Starting calculation....')
    Col_List = dataframe.columns.tolist()
    Col_List.remove('StudentID')
    Sim_Dict = {}
    logger.info(Col_List)
    start = datetime.datetime.now()
    pool = mp.Pool(10)
    for i, LO in enumerate(Col_List):
        try:

            Sim_Dict[LO] = pool.map(partial(fn.Similarity,dataframe ), zip(repeat(LO), Col_List))
            if (i%100 == 0):
                logger.info(str(LO))
                end = datetime.datetime.now()
                print("timeTaken: ", end - start)
        except socket.error as ex:
            if str(ex) == "[Errno 35] Resource temporarily unavailable":
                logger.info('socket error....')
                continue
            raise ex



    with open('dictionary.pickle', 'wb') as handle:
        pickle.dump(Sim_Dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    logger.info('Finish calculation')
    end = datetime.datetime.now()
    print("timeTaken: ", end-start)

def sum_keys(d):
    return (0 if not isinstance(d, dict)
            else len(d) + sum(sum_keys(v) for v in d.items()))

def count_values(d):
    dict_count = {}
    for k,v in d.items():
        dict_count[k] = [len([item for item in v])]
    return dict_count

if __name__ == '__main__':

    df_Student_User = pd.read_csv('df_Student_User')

    """
    Returns a list top 10  items that are similar to LO_1
    """

    SimilarityMatrix(df_Student_User)

