from player import *
from playerAI import *
from network import *

class GameMode():
    def __init__(self, manager):
        self.manager = manager
        self.player = Player()

    def draw(self):
        pass


class OfflineMode(GameMode):
    def __init__(self, manager):
        super().__init__(manager)
        self.playerAI = PlayerAI()

class OnlineMode(GameMode):
    def __init__(self, manager, serverIP):
        super().__init__(manager)
        self.network = NetWork(serverIP)


