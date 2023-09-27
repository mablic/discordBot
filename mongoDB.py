import pymongo
import random
import certifi
import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta
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

    def remove_historical_timezone(self, dict):
        try:
            criteria = {
            "$and": [
                { "userId": dict['userId'] }
            ]}
            self.studyTable.delete_many(criteria)
        except Exception as e:
            print(f"Delete many records fails: userName: {dict['userName']}")
        finally:
            pass
    
    def get_timezone_users(self):
        userDict = {}
        for itm in self.studyTable.find():
            userDict[itm['userId']] = itm
        return userDict

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

    def find_data_from_db_filter(self, filterDict):
        return self.studyTable.find(filterDict)

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

    def get_validate_check_in(self, userId, checkTime):
        result = self.studyTable.count_documents({'userId': userId, 'checkTime': checkTime})
        return result != 0

    def update_check_in(self, userId, checkTime):
        filter = {"userId": userId, "checkTime": checkTime}
        update = {"$set": {"notificationFlag": True}}
        self.studyTable.update_many(filter, update)

    def update_sdashboard_check_in(self, userId, checkTime):
        filter = {"userDiscordId": userId, "checkInTime": checkTime}
        update = {"$set": {"notificationFlag": True}}
        self.studyTable.update_many(filter, update)

    def get_my_tags(self, userName):
        pass

    def delete_all(self):
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

    # M = MongoDB()
    # M.connect_to_db('studyDB', 'dashboard_leetcode')
    # current_collection_name = "dashboard_leetcode"
    # new_collection_name = "dashboard_leetcode_archive"
    # database = M.get_collection()
    # database[current_collection_name].rename(new_collection_name, dropTarget=True)
    pass
    # M = MongoDB()
    # M.connect_to_db('studyDB', 'studyDB')
    # M.delete_all()
    # data = M.get_collection()
    # res = {}
    # for d in data.find():
    #     # print(f"d is: {type(d)}")
    #     if d['userName'] not in res.keys():
    #         res[d['userName']] = {}
    #     if d['studyTime'] not in res[d['userName']].keys():
    #         res[d['userName']][d['studyTime']] = {}
    #     for itm in d.keys():
    #         if itm != '_id' and itm != 'userName' and itm != 'studyTime':
    #             if itm not in res[d['userName']][d['studyTime']].keys():
    #                 res[d['userName']][d['studyTime']][itm] = 0
    #             res[d['userName']][d['studyTime']][itm] += d[itm]
    # def random_date(start_date, end_date):
    #     time_delta = end_date - start_date
    #     random_days = random.randint(0, time_delta.days)
    #     random_date = start_date + timedelta(days=random_days)
    #     return random_date
    # # Define the start and end dates
    # start_date = datetime(2023, 1, 1)
    # end_date = datetime(2023, 7, 31)
    # M.connect_to_db('studyDB', 'tracker_studytracker')
    # userId = "1059894715991982170"
    # for i in range(150):
    #     randomDate = datetime.strftime(random_date(start_date, end_date),"%Y-%m-%d")
    #     newDict = {
    #         'userId': "32",
    #         'userName' : "None",
    #         'discordUserId' : userId,
    #         'studyDate' : datetime.strptime(randomDate,"%Y-%m-%d"),
    #         'studyTopic' : 'Subject' + str(random.randint(1, 20)),
    #         'studyTime' : random.randint(1, 200)
    #     }
    #     M.insert_to_db(newDict)
    # for userId in res.keys():
    # userId = "1059894715991982170"
    # for userId in res.keys():
    #     for studyDate in res[userId]:
    #         for topic in res[userId][studyDate].keys():
    #             newDict = {
    #                 'userId': "None",
    #                 'userName' : "None",
    #                 'discordUserId' : userId,
    #                 'studyDate' : datetime.strptime(studyDate,"%Y-%m-%d"),
    #                 'studyTopic' : topic,
    #                 'studyTime' : res[userId][studyDate][topic]
    #             }
    #             M.insert_to_db(newDict)

    # M.update_check_in("482041455360344064", datetime.now())
    # print(M.get_validate_check_in('694765282358460519','2023-03-28'))
    # M.delete_all()
    # print(M.get_timezone_users())

    # df = pd.DataFrame({'studyTime': ['01/03/2022', '01/04/2022','01/03/2022', '01/04/2022'],'FRM': [380, 370, 24, 26], 'CFA': [np.nan, 370, np.nan, 26]})
    # df.fillna(0)
    # columns = df.columns.values.tolist()
    # res = df.groupby('studyTime')[columns].sum()
    # print('date;' + ';'.join([str(x) for x in res.columns.tolist()]))
    # for index, row in res.iterrows():
    #     nList = str(index) + ';' + ';'.join([str(x) for x in row])
    #     print(nList)
    # dateFormat = '%Y-%m-%d'
    # M = MongoDB()
    # M.connect_to_db('studyDB', 'checkDB')
    # # M.get_check_in_data('2023-01-01', '2023-12-31')
    # data = M.get_collection()

    # M.connect_to_db('studyDB', 'scheduler_checkin')
    # data = M.get_collection()
    # res = []
    # for d in data.find():
    #     # print(f"d is: {type(d)}")
    #     for itm in d.keys():
    #         if itm != '_id':
    #             res.append(d[itm])
        
    # M.connect_to_db('studyDB', 'scheduler_checkin_1')
    # for details in res:
    #     M.insert_to_db(details)
                