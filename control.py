import mongoDB
import timer
import graph
import fortune
import pandas as pd
import checkIn
from datetime import datetime, timedelta

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
        self.fortune = fortune.Fortune()
        self.checkIn = checkIn.CheckIn()
    
    def add_user(self, userName):
        self.timer.add_user(userName)
    
    def add_tag(self, userName, tagName):
        self.timer.add_tag(userName, tagName)
    
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
            self.DB.connect_to_db('studyDB', database)
        except ValueError as e:
            raise
        except Exception as e:
            print(f"Error when connect to the interview database")
            raise TypeError("Interview database not found!")

    def get_daily_notification_list(self):
        self.connect_to_any_db('scheduler_time_zone')
        timeZoneUsers = self.DB.get_timezone_users()
        self.connect_to_any_db('scheduler_checkin')
        allNotifyUser = self.DB.find_data_from_db_filter({'notificationFlag': False})
        reminderUsers = []

        for user in allNotifyUser:
            timeZone = 0
            if user['userId'] in timeZoneUsers.keys():
                timeZone = timeZoneUsers[str(user['userId'])]['timeZone']
            currentHour = datetime.strftime(datetime.now() + timedelta(hours=int(timeZone)),"%H")
            currentDay = datetime.strftime(datetime.now() + timedelta(hours=int(timeZone)),"%d")
            if int(currentHour) == 0 or int(currentDay) > int(datetime.strftime(datetime.now(), "%d")):
                reminderUsers.append(user)
                self.DB.update_check_in(user['userId'], user['checkTime'])
        return reminderUsers

    def add_checkIn(self, userId, dict):
        self.connect_to_any_db('scheduler_time_zone')
        timeZoneUsers = self.DB.get_timezone_users()
        checkInTime = datetime.strftime(datetime.now(), '%Y-%m-%d')
        if str(userId) in timeZoneUsers.keys():
            timeZone = timeZoneUsers[str(userId)]['timeZone']
            checkInTime = datetime.strftime(datetime.now() + timedelta(hours=int(timeZone)),'%Y-%m-%d')
        dict['checkTime'] = datetime.strptime(checkInTime, '%Y-%m-%d')
        dict['userMsg'] = self.fortune.get_fortune_world()
        self.connect_to_any_db('scheduler_checkin')
        if not self.DB.get_validate_check_in(userId, datetime.strptime(checkInTime, '%Y-%m-%d')):
            self.DB.insert_to_db(dict)
            self.checkIn.add_user(userId, dict)

    def remove_check_in(self, userId):
        self.checkIn.remove_users(userId)

    def get_check_in_users(self):
        return self.checkIn.get_check_in_users()

    def remove_notification(self, dict):
        self.connect_to_any_db('scheduler_notification')

    def remove_time_zone(self, dict):
        self.connect_to_any_db('scheduler_time_zone')
        self.DB.remove_historical_timezone(dict)

    def add_time_zone(self, dict):
        self.connect_to_any_db('scheduler_time_zone')
        self.DB.remove_historical_timezone(dict)
        self.DB.insert_to_db(dict)

    def add_notification(self, dict):
        self.remove_notification(dict)
        self.DB.insert_to_db(dict)
        return True

    def remove_user(self, userId):

        userDict = self.timer.remove_user(userId)
        self.connect_to_any_db('studyDB')
        self.DB.insert_to_db(userDict)
        return True

    def get_sdashboard_check_in_users(self):
        self.connect_to_any_db('dashboard_checkin')
        allUsers = self.DB.find_data_from_db_filter({'notificationFlag': False})
        
        allCheckIn = {}
        for user in allUsers:
            if user['userDiscordId'] == "None":
                continue
            if user['userDiscordId'] not in allCheckIn.keys(): 
                allCheckIn[str(user['userDiscordId'])] = []
            checkInUsers = {
                "guildId": user['checkInDiscordServer'],
                "channelId": user['checkInDiscordChannel'],
                "userId": user['userDiscordId'],
                "userName": "",
                "notificationFlag": False,
                "checkTime": user['checkInTime'],
                "questionNo": user['questionNo']
            }
            allCheckIn[str(user['userDiscordId'])].append(checkInUsers)
        
        for userId in allCheckIn.keys():
            record = allCheckIn[str(userId)][0]
            # record.pop("questionNo")
            self.DB.update_sdashboard_check_in(record['userId'], record['checkTime'])
            # self.add_checkIn(userId, record)
        return allCheckIn

    def get_time_zone_users(self):
        self.connect_to_any_db('scheduler_time_zone')
        userDict = {}
        return self.DB.get_timezone_users()

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
        return self.DB.find_all_data_from_db('hardType', type)

    def remove_file(self, filePath):
        self.graph.remove_file(filePath)

    def get_scheduler_notification(self):
        try:
            self.connect_to_any_db('scheduler_notification')
            allSchedulerUsers = self.DB.get_collection()
            self.DB.connect_to_db('studyDB', 'scheduler_time_zone')
            allTimeZoneUsers = self.DB.get_timezone_users()
        except Exception as e:
            print(str(e))
            return
        result = {}
        for user in allSchedulerUsers.find():
            timeZone = 0
            if user['userId'] in allTimeZoneUsers.keys():
                timeZone = allTimeZoneUsers[str(user['userId'])]['timeZone']
            checkInTime = datetime.strftime(datetime.now() + timedelta(hours=int(timeZone)),'%H')
            if int(checkInTime) >= int(user['time']):
                if str(user['userId']) not in result.keys():
                    result[user['userId']] = user
        return result


    def __del__(self):
        pass

if __name__ == '__main__':
    pass
    # m = Control()
    # m.get_check_in_graph('2023-03-06', '2023-03-12')
    # newDict = {'userName':'mai','channelName':'123','time':'9','message':'妈妈', 'userId': '12312312'}
    # print(m.get_notification())
    # print(m.get_linkCode_question('easy'))
    # print(m.get_data_graph('482041455360344064', 'pie', 'day', '2022-01-17'))
    # m.get_data_graph('482041455360344064', 'pie', 'day')