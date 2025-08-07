from player import *
from bot import *
from network import *
import random
from mySignal import *
from screenmanager import *

class GameMode():
    def __init__(self, manager):
        self.manager = manager
        self.player = Player()

    def draw(self):
        pass


class OfflineMode(GameMode):
    def __init__(self, manager):
        super().__init__(manager)
        self.playerAI = Bot()

class OnlineMode(GameMode):
    def __init__(self, manager, serverIP):
        super().__init__(manager)
        self.network = NetWork(serverIP)
        self.roomID = None
        self.type = None

    def changeTurn(self):
        pass

    def createRoom(self):
        self.roomID = random.randint(10000, 99999)
        return self.roomID

    def joinRoom(self):
        pass

    def running(self):
        if self.type == None:
            return
        newSignal = SignalSended(self.type, self.roomID)
        respon = self.network.send(newSignal)
        if respon.phase == "PREPARE":
            self.manager.changeScreen(PrepareScreen())




