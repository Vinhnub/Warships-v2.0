from screen import *
from player import *
from gamemode import *

class Main():
    def __init__(self, window):
        self.window = window
        self.currentScreen = MenuScreen(self, self.window)
        self.game = None

    def changeScreen(self, newScreen):
        self.currentScreen = newScreen

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
        if self.game:
            self.game.draw()