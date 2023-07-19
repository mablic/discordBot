class SyncBot:

    __instance = 0

    def __new__(cls):

        if cls.__instance == 0:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self._setBotToWait = False
        self._waitTime = 1

    @property
    def setBotToWait(self):
        return self._setBotToWait
    
    @setBotToWait.setter
    def setBotToWait(self, val):
        if isinstance(val, bool):
            self._setBotToWait = val

    @property
    def waitTime(self):
        return self._waitTime

    @waitTime.setter
    def waitTime(self, val):
        if isinstance(val, int):
            self._waitTime = val