import fortune
from datetime import datetime
from datetime import timedelta
from random import randint

class CheckIn:

    __instance = None

    def __new__(cls):
        
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:

        self.dict = {}
        self.dateFormat = '%Y-%m-%d'

    def add_user(self, channelId, userId, userName):
        newFortune = fortune.Fortune()
        if channelId not in self.dict.keys():
            self.dict[channelId] = {}
        if userId not in self.dict[channelId]:        
            self.dict[channelId][userId] = userName + newFortune.get_fortune_world()
        else:
            return

    def check_to_db(self):
        yesterday = datetime.strftime(datetime.now() - timedelta(days=1), self.dateFormat)
        importDict = {}
        for channel in self.dict.keys():
            for user in self.dict[channel]:
                if user not in importDict.keys():
                    importDict[user] = {}
                    importDict[user]['checkChannels'] = []
                importDict[user]['checkTime'] = yesterday
                importDict[user]['checkChannels'].append(str(channel))
                importDict[user]['checkDetails'] = self.dict[channel][user]
        self.remove_users()
        return importDict

    def get_users(self):
        return self.dict

    def remove_users(self):
        self.dict = {}


if __name__ ==  '__main__':

    pass
