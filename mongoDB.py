import pymongo
import certifi
import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient
sys.path.insert(1,os.getcwd() + '/web_app')

class Table:
    studyDB = 'studyDB'

class MongoDB:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.collection = None

    def connect_to_db(self):
        connectionString = os.environ.get('MONGODB_CONNECTION')
        cluster = MongoClient(connectionString, tlsCAFile=certifi.where())
        db = cluster['studyDB']
        self.studyTable = db[Table.studyDB]

    def insert_to_db(self, userDict):
        self.studyTable.insert_one(userDict)

    def find_data_from_db(self, userName):
        return self.studyTable.find({'userName': userName})
    
    def get_my_tags(self, userName):
        pass

    def delete_all(self):
        self.studyTable.delete_many({})
        self.studyTable.delete_many({})
    def __del__(self):
        pass

if __name__ == '__main__':

    pass
    # df = pd.DataFrame({'studyTime': ['01/03/2022', '01/04/2022','01/03/2022', '01/04/2022'],'FRM': [380, 370, 24, 26], 'CFA': [np.nan, 370, np.nan, 26]})
    # df.fillna(0)
    # columns = df.columns.values.tolist()
    # res = df.groupby('studyTime')[columns].sum()
    # print('date;' + ';'.join([str(x) for x in res.columns.tolist()]))
    # for index, row in res.iterrows():
    #     nList = str(index) + ';' + ';'.join([str(x) for x in row])
    #     print(nList)
