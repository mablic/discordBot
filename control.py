import mongoDB
import timer
import graph
import pandas as pd
from datetime import datetime

class Control:
    
    __instance = None

    def __new__(cls):
        
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.DB = mongoDB.MongoDB()
        self.anyDB = mongoDB.MongoDB()
        self.timer = timer.Timer()
        self.graph = graph.Graph()
    
    def add_user(self, userName):
        self.timer.add_user(userName)
    
    def add_tag(self, userName, tagName):
        self.timer.add_tag(userName, tagName)
    
    def remove_checkIn(self, dict):
        try:
            self.DB.connect_to_db('studyDB', 'checkDB')
        except Exception as e:
            print(str(e))
            return False
        self.DB.insert_to_db(dict)
        return True

    def remove_notification(self, dict):
        try:
            self.anyDB.connect_to_db('studyDB', 'scheduler_notification')
            self.anyDB.remove_historical_scheduler(dict)
        except Exception as e:
            print(str(e))
        finally:
            pass

    def add_notification(self, dict):
        self.remove_notification(dict)
        self.anyDB.insert_to_db(dict)
        return True

    def remove_user(self, userId):

        userDict = self.timer.remove_user(userId)
        try:
            self.DB.connect_to_db('studyDB','studyDB')
        except Exception as e:
            print(str(e))
            return False
        self.DB.insert_to_db(userDict)
        return True

    def connect_to_db(self, userName):
        try:
            self.DB.connect_to_db('studyDB','studyDB')
            self.graph = graph.Graph()
            data = self.DB.find_data_from_db(userName)
        except ValueError as e:
            raise
        except Exception as e:
            print(f"Error with userName {userName}")
            raise TypeError("No user found!")
        return data

    #dashboard_leetcode
    def connect_to_any_db(self, database):
        try:
            self.anyDB.connect_to_db('studyDB', database) #'dashboard_leetcode')
        except ValueError as e:
            raise
        except Exception as e:
            print(f"Error when connect to the interview database")
            raise TypeError("Interview database not found!")

    def get_data_details(self, userName):
        try:
            data = self.connect_to_db(userName)
        except Exception as e:
            raise
        df = pd.DataFrame(list(data))
        df.fillna(0)
        columns = df.columns.values.tolist()
        df = df.groupby('studyTime')[columns].sum()
        response = []
        response.append('DATE;' + ';'.join([str(x) for x in df.columns.tolist()]))
        for index, row in df.iterrows():
            nList = str(index) + ';' + ';'.join([str(x) for x in row])
            response.append(nList)
        return response

    def get_data_graph(self, userName, graphType, interval='day', day=datetime.strftime(datetime.now(),'%Y-%m-%d')):
        try:
            data = self.connect_to_db(userName)
        except Exception as e:
            raise
        df = pd.DataFrame(list(data))
        df.fillna(0, inplace=True)
        df.drop(columns=['_id', 'userName'], inplace=True)

        if graphType == 'pie':
            return self.graph.get_public_graph(df, userName, day)
        else:
            return self.graph.get_graph(df, userName, interval, graphType)

    def get_check_in_graph(self, startDate, endDate):
        data = self.DB.get_check_in_data(startDate, endDate)
        self.graph.graph_check_in(data)

    def get_linkCode_question(self, type='all'):
        self.connect_to_any_db('dashboard_leetcode')
        type = type[0].upper() + type[1:]
        return self.anyDB.find_all_data_from_db('hardType', type)

    def remove_file(self, filePath):
        self.graph.remove_file(filePath)

    def get_notification(self):
        self.connect_to_any_db('scheduler_notification')
        return self.anyDB.get_notification()

    def __del__(self):
        pass

if __name__ == '__main__':
    pass
    # m = Control()
    # m.get_check_in_graph('2023-02-20', '2023-02-26')
    # newDict = {'userName':'mai','channelName':'123','time':'9','message':'妈妈', 'userId': '12312312'}
    # print(m.get_notification())
    # print(m.get_linkCode_question('easy'))
    # print(m.get_data_graph('482041455360344064', 'pie', 'day', '2022-01-17'))
    # m.get_data_graph('482041455360344064', 'pie', 'day')