import mongoDB
import timer
import graph
import pandas as pd
import asyncio
from datetime import datetime

class Control:
    
    __instance = None

    def __new__(cls):
        
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.DB = mongoDB.MongoDB()
        self.timer = timer.Timer()
        self.graph = graph.Graph()
    
    def add_user(self, userName):
        self.timer.add_user(userName)
    
    def add_tag(self, userName, tagName):
        self.timer.add_tag(userName, tagName)
    
    def remove_user(self, userName):

        userDict = self.timer.remove_user(userName)
        try:
            self.DB.connect_to_db()
        except Exception as e:
            print(str(e))
            return False
        self.DB.insert_to_db(userDict)
        return True

    def connect_to_db(self, userName):
        try:
            self.DB.connect_to_db()
            self.graph = graph.Graph()
            data = self.DB.find_data_from_db(userName)
        except ValueError as e:
            raise
        except Exception as e:
            print(f"Error with userName {userName}")
            raise TypeError("No user found!")
        return data

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

    def remove_file(self, filePath):
        self.graph.remove_file(filePath)

    def __del__(self):
        pass

if __name__ == '__main__':
    pass
    # m = Control()
    # print(m.get_data_graph('482041455360344064', 'pie', 'day', '2022-01-17'))
    # m.get_data_graph('482041455360344064', 'pie', 'day')