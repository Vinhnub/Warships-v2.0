class Screen():
    def __init__(self):
        pass

    def handleEvent(self):
        pass
    
    def update(self):
        pass

    def draw(self):
        pass

class MenuScreen(Screen):
    pass

class ScreenManager():
    def __init__(self):
        self.currentScreen = MenuScreen()

    def changeScreen(self, newScreen):
        self.currentScreen = newScreen

    def draw(self):
        self.currentScreen.draw()

    