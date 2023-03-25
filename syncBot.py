class SyncBot:

    __instance = 0

    def __new__(cls):

        if cls.__instance == 0:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self._botHourWait = 0
        self._waitTime = 1
        self._notifyTime = 1
        self._checkRun = 0

    @property
    def botHourWait(self):
        return self._botHourWait
    
    @botHourWait.setter
    def botHourWait(self, val):
        if isinstance(val, int):
            self._botHourWait += val
    
    @property
    def checkRun(self):
        return self._checkRun

    @checkRun.setter
    def checkRun(self, val):
        if isinstance(val, int):
            self._checkRun = val

    @property
    def waitTime(self):
        return self._waitTime

    @waitTime.setter
    def waitTime(self, val):
        if isinstance(val, int):
            self._waitTime = val
    
    @property
    def notifyTime(self):
        return self._notifyTime
    
    @notifyTime.setter
    def notifyTime(self, val):
        self._notifyTime = val

    def stop_bot(self):
        return self._botHourWait == self._checkRun