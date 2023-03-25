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

    def add_user(self, guildId, channelId, userId, userName):
        newFortune = fortune.Fortune()
        # if channelId not in self.dict.keys():
        #     self.dict[channelId] = {}
        userId = str(userId)
        channelId = str(channelId)
        guildId = str(guildId)
        if userId not in self.dict.keys():
            self.dict[userId] = {}
        if guildId not in self.dict[userId]:    
            self.dict[userId][guildId] = {}
            self.dict[userId][guildId]['details'] = userName + newFortune.get_fortune_world()
            self.dict[userId][guildId]['guildId'] = guildId
            self.dict[userId][guildId]['channelId'] = channelId
            self.dict[userId][guildId]['userId'] = userId
            self.dict[userId][guildId]['userName'] = userName
        else:
            return

    def check_to_db(self, userId, checkTime):
        userId = str(userId)
        importDict = {}
        if userId in self.dict.keys():
            yesterday = datetime.strftime(checkTime + timedelta(days=-1), self.dateFormat)
            for guildId in self.dict[userId]:
                self.dict[userId][guildId]['checkTime'] = yesterday
            importDict = self.dict[userId]
            # importDict.pop('_id')
            self.dict.pop(userId)
        return importDict

    def get_users(self):
        return self.dict

    def remove_users(self):
        self.dict = {}


if __name__ ==  '__main__':
    pass
    # C = CheckIn()
    # C.add_user('1','2','mablic')
    # C.check_to_db({'2': 1})
