from listPath import *
from widget import *
from abc import abstractmethod
from player import *
from network import *
import pygwidgets
from bot import *
import random
from mySignal import *
from constants import *

#============================================================ SCREEN MANAGER ============================================================

class Screen():
    @abstractmethod
    def __init__(self, screenManager, window):
        self.screenManager = screenManager
        self.window = window
    
    @abstractmethod
    def handleEvent(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class MenuScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
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
            #self.inputData = InputData(self.window, (400, 250))
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game = OnlineMode(self.screenManager, '26.253.176.29')
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


class CreateRoom(Screen):
    def __init__(self, screenManager, window, roomID):
        super().__init__(screenManager, window)
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
        super().__init__(screenManager, window)
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
        super().__init__(screenManager, window)
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


class PrepareScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.readyBtn = AnimatedButton(self.window, (500, 700), [resource_path("assets/images/buttons/readyBtn_u.png")], [resource_path("assets/images/buttons/readyBtn_d.png")], [resource_path("assets/images/buttons/readyBtn_dis.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/mainscreen/mainscreen_1.png")])

    def handleEvent(self, event):
        if self.readyBtn.handleEvent(event):
            self.readyBtn.disable()
            self.screenManager.game.ready()
    
    def draw(self):
        self.background.draw()
        self.field.draw()
        self.readyBtn.draw()
        self.screenManager.game.player.draw(self.window)

class MyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.timer = None

    def handleEvent(self, event):
        pass

    def draw(self):
        self.field.draw()
        self.screenManager.game.player.draw(self.window, True)

class EnemyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.timer = None

    def handleEvent(self, event):
        pass

    def draw(self):
        self.field.draw()
        self.screenManager.game.player.draw(self.window, False)



# ============================================================ MODE ============================================================

class OfflineMode():
    def __init__(self, manager):
        self.manager = manager
        self.player = Player()
        self.playerAI = Bot()

class OnlineMode():
    def __init__(self, manager, serverIP):
        self.manager = manager
        self.player = Player(self.manager.window)
        self.network = NetWork(serverIP)
        self.roomID = None
        self.type = None
        self.data = None

    def createRoom(self):
        self.roomID = str(random.randint(10000, 99999))
        return self.roomID
    
    def ready(self):
        self.type = "READY"
        self.data = self.player.calListPosShip()
        self.player.isReady = True

    def running(self, event):
        if self.type is None or self.roomID is None or self.roomID == "":
            return
        newSignal = SignalSended(self.type, self.roomID, self.data)
        respon = self.network.send(newSignal)
        if respon.phase == "PREPARE":
            if not isinstance(self.manager.currentScreen, PrepareScreen):
                self.manager.changeScreen(PrepareScreen(self.manager, self.manager.window))
                self.type = "WAITING_PR"
                self.data = None
            self.player.handleEvent(event)

        if respon.phase == "PLAYING":
            if respon.turnIP == respon.playerIP:
                if not isinstance(self.manager.currentScreen, MyTurnScreen):
                    self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))
                    self.player.canFire = True
                    self.type = "WAITING_PL"
                    self.data = len(self.player.listEnemyTorpedo)
                
                res = self.player.handleEvent(event)
                if res:
                    self.player.canFire = False
                    self.type = "FIRE"
                    self.data = res

                if respon.type == "FIRERESULT":
                    self.player.listMyTorpedo.append(Torpedo(self.manager.window, self.data, listPathTopedoA, pathImageTorpedo, respon.data, 100))
                    self.type = "WAITING_PL"
                    self.data = len(self.player.listEnemyTorpedo)

            else:
                if not isinstance(self.manager.currentScreen, EnemyTurnScreen):
                    self.manager.changeScreen(EnemyTurnScreen(self.manager, self.manager.window))
                    self.type = "WAITING_PL"
                    self.canFire = True
    
                self.data = len(self.player.listEnemyTorpedo)
                
                if respon.type == "ENEMYFIRE":
                    if self.canFire:
                        self.player.listEnemyTorpedo.append(Torpedo(self.manager.window, respon.data, listPathTopedoA, pathImageTorpedo, self.player.isCorrect(respon.data), 100))
                        self.canFire = False


    def draw(self):
        pass



