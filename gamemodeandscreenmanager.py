from listPath import *
from widget import *
from abc import abstractmethod
from player import *
from network import *
import pygwidgets
from bot import *
import random
from mySignal import *

class Screen():
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def handleEvent(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class MenuScreen(Screen):
    def __init__(self, screenManager, window):
        self.screenManager = screenManager
        self.window = window
        self.exitBtn = AnimatedButton(self.window, (550, 450), [resource_path("assets/images/buttons/exitBtn_u.png")], [resource_path("assets/images/buttons/exitBtn_d.png")])
        self.onlBtn = AnimatedButton(self.window, (375, 250), [resource_path("assets/images/buttons/onlBtn_u.png")], [resource_path("assets/images/buttons/onlBtn_d.png")])
        self.offBtn = AnimatedButton(self.window, (375, 350), [resource_path("assets/images/buttons/offBtn_u.png")], [resource_path("assets/images/buttons/offBtn_d.png")])
        self.image = [AnimatedImage(self.window, (0, 0), path) for path in listPathImageMenuScreen]
        self.inputData = None
        self.warning = None
    
    def draw(self):
        for item in self.image:
            item.draw()
        self.onlBtn.draw()
        self.offBtn.draw()
        self.exitBtn.draw()
        if self.inputData is not None:
            self.inputData.draw()


    def handleEvent(self, event):
        if self.exitBtn.handleEvent(event):
            pygame.quit()
            sys.exit()
        if self.onlBtn.handleEvent(event):
            self.onlBtn.disable()
            self.offBtn.disable()
            self.exitBtn.disable()
            self.inputData = InputData(self.window, (400, 250))
        if self.offBtn.handleEvent(event):
            self.screenManager.game = OfflineMode(self.screenManager)
        if self.inputData is not None:
            res = self.inputData.handleEvent(event) 
            if res[0] == -1:
                self.onlBtn.enable()
                self.offBtn.enable()
                self.exitBtn.enable()
                self.inputData = None
            elif res[0] == 1:
                self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
                self.screenManager.game = OnlineMode(self.screenManager, res[1])

class PrepareScreen(Screen):
    def __init__(self, screenManager, window):
        self.screenManager = screenManager
        self.window = window

    def handleEvent(self, event):
        pass
    
    def draw(self):
        pass

class PlayingScreen(Screen):
    pass

class CreateRoom(Screen):
    def __init__(self, screenManager, window, roomID):
        self.window = window
        self.screenManager = screenManager
        self.roomIDText = CustomText(window, (500, 350), roomID, resource_path("fonts/PressStart2P-Regular.ttf"), font_size=50, color=(255, 255, 255))
        self.backBtn = AnimatedButton(self.window, (550, 450), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])

    def handleEvent(self, event):
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game.type = None
            self.screenManager.game.roomID = None

    def draw(self):
        self.roomIDText.draw()
        self.backBtn.draw()

class JoinRoom(Screen):
    def __init__(self, screenManager, window):
        self.screenManager = screenManager
        self.window = window
        self.roomIDInput = pygwidgets.InputText(self.window, (500, 400), fontSize=50, width=300)
        self.backBtn = AnimatedButton(self.window, (550, 450), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])
        self.enterBtn = AnimatedButton(self.window, (550, 550), [resource_path("assets/images/buttons/enterBtn_u.png")], [resource_path("assets/images/buttons/enterBtn_d.png")])

    def handleEvent(self, event):
        self.roomIDInput.handleEvent(event)
        if self.enterBtn.handleEvent(event):
            self.screenManager.game.roomID = self.roomIDInput.getValue()
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game.type = None
            self.screenManager.game.roomID = None

    def draw(self):
        self.backBtn.draw()
        self.roomIDInput.draw()
        self.enterBtn.draw()
        

class FindingScreen(Screen):
    def __init__(self, screenManager, window):
        self.screenManager = screenManager
        self.window = window
        self.createBtn = AnimatedButton(self.window, (500, 250), [resource_path("assets/images/buttons/createBtn_u.png")], [resource_path("assets/images/buttons/createBtn_d.png")])
        self.joinBtn = AnimatedButton(self.window, (550, 350), [resource_path("assets/images/buttons/joinBtn_u.png")], [resource_path("assets/images/buttons/joinBtn_d.png")])
        self.backBtn = AnimatedButton(self.window, (550, 450), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])
        self.image = [AnimatedImage(self.window, (0, 0), path) for path in listPathImageMenuScreen]
        self.warning = None

    def draw(self):
        for item in self.image:
            item.draw()
        self.createBtn.draw()
        self.joinBtn.draw()
        self.backBtn.draw()
        
    def handleEvent(self, event):
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(MenuScreen(self.screenManager, self.window))
            self.screenManager.player = None
        if self.createBtn.handleEvent(event):
            self.screenManager.game.type = "CREATEROOM"
            self.screenManager.changeScreen(CreateRoom(self.screenManager, self.window, self.screenManager.game.createRoom()))
        if self.joinBtn.handleEvent(event):
            self.screenManager.game.type = "JOINROOM"
            self.screenManager.changeScreen(JoinRoom(self.screenManager, self.window))

class OfflineMode():
    def __init__(self, manager):
        super().__init__(manager)
        self.playerAI = Bot()

class OnlineMode():
    def __init__(self, manager, serverIP):
        self.manager = manager
        self.player = Player()
        self.network = NetWork(serverIP)
        self.roomID = None
        self.type = None

    def changeTurn(self):
        pass

    def createRoom(self):
        self.roomID = str(random.randint(10000, 99999))
        return self.roomID

    def joinRoom(self):
        pass

    def running(self):
        if self.type is None or self.roomID is None or self.roomID == "":
            return
        newSignal = SignalSended(self.type, self.roomID)
        respon = self.network.send(newSignal)
        if respon.phase == "PREPARE":
            self.manager.changeScreen(PrepareScreen(self.manager, self.manager.window))

    def draw(self):
        pass


