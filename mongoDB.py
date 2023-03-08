import pymongo
import random
import certifi
import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime
sys.path.insert(1,os.getcwd() + '/web_app')


class MongoDB:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.collection = None
        self.dateFormat = '%Y-%m-%d'

    def connect_to_db(self, clusterName='studyDB', table='studyDB'):
        # pass
        try:
            connectionString = os.environ.get('MONGODB_CONNECTION')
            cluster = MongoClient(connectionString, tlsCAFile=certifi.where())
            db = cluster[clusterName]
        except Exception as e:
            print(f"Not able to connect to the DB {str(e)}")
            raise ValueError("No DB Connection!")
        self.studyTable = db[table]

    def get_collection(self):
        return self.studyTable

    def get_notification(self):
        remindDict = {}
        for itm in self.studyTable.find():
            channelId = itm['channelId']
            nTime = itm['time']
            userName = itm['userName']
            userMessage = '妈妈喊你打卡啦!' if not itm['message']  else itm['message']
            if channelId not in remindDict.keys():
                remindDict[channelId] = {}
            if nTime not in remindDict[channelId].keys():
                remindDict[channelId][nTime] = []
            remindDict[channelId][nTime].append([userName, userMessage])
        return remindDict
                
    def remove_historical_scheduler(self, dict):
        try:
            criteria = {
            "$and": [
                { "userName": dict['userName'] },
                { "channelId": dict['channelId'] }
            ]}
            self.studyTable.delete_many(criteria)
        except Exception as e:
            print(f"Delete many records fails: userName: {dict['userName']}; channel id: {dict['channelId']}")
        finally:
            pass

    def insert_to_db(self, userDict):
        if not bool(userDict):
            return
        try:
            self.studyTable.insert_one(userDict)
        except Exception as e:
            print(f"Not able to insert data: {e}")
        finally:
            pass

    def find_data_from_db(self, userName):
        return self.studyTable.find({'userName': userName})

    def find_all_data_from_db(self, field1 = '', filter= ''):
        # print(field1 + ' ' + filter)
        if filter == 'All':
            curSor = self.studyTable.find()
        else:
            curSor = self.studyTable.find({field1: filter})
        ret = []
        for cur in curSor:
            ret.append(dict(cur))
        res = ret[random.randint(1, len(ret))]
        return res['link']

    def get_my_tags(self, userName):
        pass

    def delete_all(self):
        self.studyTable.delete_many({})
        self.studyTable.delete_many({})
    def __del__(self):
        pass

    def get_check_in_data(self, startDate, endDate):
        startDate = datetime.strptime(startDate, self.dateFormat)
        endDate = datetime.strptime(endDate, self.dateFormat)
        self.connect_to_db('studyDB', 'checkDB')

        userDict = {}
        for d in self.studyTable.find():
            for itm in d.keys():
                if itm != '_id':
                    date = d[itm]['checkTime']
                    if datetime.strptime(date, self.dateFormat) < startDate or datetime.strptime(date, self.dateFormat) > endDate:
                        break
                    else:
                        userName = date = d[itm]['checkDetails']
                        findName = userName.find('>>>')
                        userName = userName[:findName]
                        if userName in userDict.keys():
                            userDict[userName] += 1
                        else:
                            userDict[userName] = 1
        return userDict

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
    # startDate = datetime(2023, 1, 1, 0, 0, 0, 0)
    # endDate = datetime(2023, 12, 31, 0, 0, 0, 0)
    # dateFormat = '%Y-%m-%d'
    # M = MongoDB()
    # print(M.get_check_in_data('2023-01-01', '2023-12-31'))
    # M.connect_to_db('studyDB', 'checkDB')
    # data = M.get_collection()

    # userDict = {}

    # for d in data.find():
    #     # print(f"d is: {type(d)}")
    #     for itm in d.keys():
    #         if itm != '_id':
    #             date = d[itm]['checkTime']
    #             if datetime.strptime(date, dateFormat) < startDate or datetime.strptime(date, dateFormat) > endDate:
    #                 break
    #             else:
    #                 userName = date = d[itm]['checkDetails']
    #                 findName = userName.find('>>>')
    #                 userName = userName[:findName]
    #                 if userName in userDict.keys():
    #                     userDict[userName] += 1
    #                 else:
    #                     userDict[userName] = 1

    # # Print the results
    # for key, value in userDict.items():
    #     print(f"userName is: {key} the count is {value}")