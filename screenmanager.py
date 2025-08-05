from listPath import *
from widget import *
from abc import abstractmethod

class Screen():
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def handleEvent(self):
        pass
    
    # def update(self):
    #     pass

    @abstractmethod
    def draw(self):
        pass

class MenuScreen(Screen):
    def __init__(self, window):
        self.window = window
        self.exitBtn = AnimatedButton(self.window, (550, 450), [resource_path("assets/images/buttons/exitBtn_u.png")], [resource_path("assets/images/buttons/exitBtn_d.png")])
        self.onlBtn = AnimatedButton(self.window, (375, 250), [resource_path("assets/images/buttons/onlBtn_u.png")], [resource_path("assets/images/buttons/onlBtn_d.png")])
        self.offBtn = AnimatedButton(self.window, (375, 350), [resource_path("assets/images/buttons/offBtn_u.png")], [resource_path("assets/images/buttons/offBtn_d.png")])
        self.image = [AnimatedImage(self.window, (0, 0), path) for path in listPathImageMenuScreen]
    
    def draw(self):
        for item in self.image:
            item.draw()
        self.onlBtn.draw()
        self.offBtn.draw()
        self.exitBtn.draw()

    def handleEvent(self, event):
        if self.exitBtn.handleEvent(event):
            pygame.quit()
            sys.exit()
        if self.onlBtn.handleEvent(event):
            print(1)
        if self.offBtn.handleEvent(event):
            print(2)



class PrepareScreen(Screen):
    pass

class PlayingScreen(Screen):
    pass

class FindingScreen(Screen):
    pass

class ScreenManager():
    def __init__(self, window):
        self.window = window
        self.currentScreen = MenuScreen(self.window)

    def changeScreen(self, newScreen):
        self.currentScreen = newScreen

    def handleEvent(self, event):
        self.currentScreen.handleEvent(event)
    
    def draw(self):
        self.currentScreen.draw()

    

    