import mongoDB
import timer
import graph
import pandas as pd
import asyncio

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
        self.DB.connect_to_db()
        self.DB.insert_to_db(userDict)

    def get_data_details(self, userName):
        self.DB.connect_to_db()
        data = self.DB.find_data_from_db(userName)
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

    def get_data_graph(self, userName, interval, graphType):
        self.DB.connect_to_db()
        self.graph = graph.Graph()
        data = self.DB.find_data_from_db(userName)
        df = pd.DataFrame(list(data))
        df.fillna(0, inplace=True)
        df.drop(columns=['_id', 'userName'], inplace=True)
        return self.graph.get_graph(df, userName, interval, graphType)

    def remove_file(self, filePath):
        self.graph.remove_file(filePath)

    def __del__(self):
        pass

if __name__ == '__main__':
    pass
    # m = Control()

    # async def runCode():
    #     divs1 = loop.create_task(m.get_data_graph('482041455360344064', 'month', 'bar'))
    #     divs2 = loop.create_task(m.get_data_graph('482041455360344064', 'week', 'bar'))
    #     divs3 = loop.create_task(m.get_data_graph('482041455360344064', 'day', 'bar'))
    #     await asyncio.wait([divs1,divs2,divs3])
    # # async def runCode():
    # #     m.get_data_graph('482041455360344064', 'month', 'bar')
    # #     m.get_data_graph('482041455360344064', 'week', 'bar')
    # #     m.get_data_graph('482041455360344064', 'day', 'bar')
    # try:
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(runCode())
    # except Exception as e:
    #     pass
    # finally:
    #     loop.close()