from ship import *
from torpedo import *
from radar import *

class Player():
    def __init__(self, mode=False): # mode: false: offline, true: online
        self.listShip = []
        self.__listTorpedo = []
        self.__listEnemyTorpedo = []
        self.radar = Radar() if mode else None

    def appendTorpedo(self, newTorpedo):
        self.__listTorpedo.append(newTorpedo)

    def appendEnemyTorpedo(self, newTorpedo):
        self.__listEnemyTorpedo.append(newTorpedo)    