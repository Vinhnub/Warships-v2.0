from screenmanager import *
from player import *

class Main():
    def __init__(self, window):
        self.window = window
        self.currentScreen = MenuScreen(self, self.window)
        self.game = None

    def changeScreen(self, newScreen):
        self.currentScreen = newScreen

    def handleEvent(self, event):
        self.currentScreen.handleEvent(event)
    
    def draw(self):
        self.currentScreen.draw()
        if self.game:
            self.game.draw()