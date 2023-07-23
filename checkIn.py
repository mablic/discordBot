from datetime import datetime
from datetime import timedelta
from random import randint

# DO NOT  USED
class CheckIn:

    __instance = None

    def __new__(cls):
        
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:

        self.dict = {}
        self.dateFormat = '%Y-%m-%d'

    def add_user(self, userId, dict):
        if userId not in self.dict.keys():
            self.dict[userId] = dict

    def remove_users(self, userId):
        if userId in self.dict.keys():
            self.dict.pop(userId)

    def get_check_in_users(self):
        return self.dict

if __name__ ==  '__main__':
    pass
    # C = CheckIn()
    # C.add_user('1','2','userID','mablic')
    # C.check_to_db({'2': 1})
