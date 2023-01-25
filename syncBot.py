class SyncBot:

    __instance = 0

    def __new__(cls):

        if cls.__instance == 0:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self._botWait = 0
        self._waitTime = 1

    @property
    def botWait(self):
        return self._botWait
    
    @botWait.setter
    def botWait(self, val):
        self._botWait = val
    
    @property
    def waitTime(self):
        return self._waitTime

    @waitTime.setter
    def waitTime(self, val):
        if isinstance(val, int):
            self._waitTime = val