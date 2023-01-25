import time
import mongoDB
from datetime import datetime

class Timer:
    __instance = None
    __count = 0

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__count += 1
        return cls.__instance

    @classmethod
    def get_count(cls):
        print(cls.__count)

    def __init__(self) -> None:
        self.userDict = {}
        self.db = mongoDB.MongoDB()
        self.dateFormat = "%Y-%m-%d"

    def add_user(self, userName):
        if userName not in self.userDict.keys():
            newUserDict = {}
            newUserDict['userName'] = userName
            newUserDict['startTime'] = datetime.now()
            newUserDict['studyTime'] = datetime.strftime(datetime.now(), self.dateFormat)
            self.userDict[userName] = newUserDict
        else:
            if 'startTime' not in self.userDict[userName]:
                # print(f" {userName} already in the dictionary!")
                self.userDict[userName]['startTime'] = datetime.now()
                self.userDict[userName]['studyTime'] = datetime.now()

    def add_tag(self, userName, tagName):
        if userName not in self.userDict.keys():
            # print(f" User add_Tag {userName} was not in the dict!")
            return
        
        if 'studyTag' in self.userDict[userName]:
            startTime = self.userDict[userName]['startTime']
            endTime = datetime.now()
            totalTime = round((endTime - startTime).total_seconds() / 60, 2)
            self.userDict[userName][self.userDict[userName]['studyTag']] = totalTime
            self.userDict[userName]['startTime'] = endTime
            self.userDict[userName].pop('studyTag')
        self.userDict[userName]['studyTag'] = tagName

    def remove_user(self, userName):
        if userName not in self.userDict.keys():
            # print(f" User remove_user {userName} was not in the dict!")
            return

        startTime = self.userDict[userName]['startTime']
        endTime = datetime.now()
        totalTime = round((endTime - startTime).total_seconds() / 60, 2)
        if 'studyTag' not in self.userDict[userName]:
            self.userDict[userName]['study'] = totalTime
        else:
            self.userDict[userName][self.userDict[userName]['studyTag']] = totalTime
            self.userDict[userName].pop('studyTag')
        self.userDict[userName].pop('startTime')
        returnDict = self.userDict[userName]
        self.userDict.pop(userName)
        return returnDict


    def __del__(self):
        pass

if __name__ == '__main__':

    pass

    # DB = mongoDB.MongoDB()
    # DB.connect_to_db()

    # instance1 = Timer()
    # instance1.add_user('Mai')
    # instance1.add_user('Ying')
    # instance1.add_tag('Mai', 'LeetCode')
    # instance1.add_tag('Ying', 'Coding')
    # time.sleep(1)
    # instance1.add_user('Mai')
    # instance1.add_tag('Mai', 'FRM')
    # time.sleep(2)
    # userDict = instance1.remove_user('Mai')

    # DB.insert_to_db(userDict)
