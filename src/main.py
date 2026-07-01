from screen import *
from player import *
from gamemode import *

class Main():
    def __init__(self, window):
        self.window = window
        self.currentScreen = MenuScreen(self, self.window)
        self.game = None
        self.fireTorpedoSound = None
        self.fireRadarSound = None

    def changeScreen(self, newScreen):
        self.currentScreen = newScreen

    def gameMode(self):
        if self.game is None: return
        return isinstance(self.game, OnlineMode)

    def onlineMode(self, ip):
        self.game = OnlineMode(self, ip)

    def offlineMode(self):
        self.game = OfflineMode(self)

    def handleEvent(self, event):
        self.currentScreen.handleEvent(event)
        if self.game:
            self.game.running(event)
    
    def draw(self):
        self.currentScreen.draw()