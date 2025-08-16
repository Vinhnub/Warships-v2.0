from listPath import *
from widget import *
from abc import abstractmethod
from player import *
from network import *
import pygwidgets
from mySignal import *
from constants import *
from radar import *

#============================================================ SCREEN MANAGER ============================================================

class Screen():
    @abstractmethod
    def __init__(self, screenManager, window):
        self.screenManager = screenManager
        self.window = window
        self.warning = None
        self.banner = []
    
    @abstractmethod
    def handleEvent(self, event):
        pass

    @abstractmethod
    def draw(self):
        for item in self.banner:
            item.draw()
        if self.warning is not None:
            if not self.warning.draw():
                self.warning = None



class MenuScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.exitBtn = AnimatedButton(self.window, (650, 520), [resource_path("assets/images/buttons/exitBtn_u.png")], [resource_path("assets/images/buttons/exitBtn_d.png")])
        self.onlBtn = AnimatedButton(self.window, (475, 280), [resource_path("assets/images/buttons/onlBtn_u.png")], [resource_path("assets/images/buttons/onlBtn_d.png")])
        self.offBtn = AnimatedButton(self.window, (475, 400), [resource_path("assets/images/buttons/offBtn_u.png")], [resource_path("assets/images/buttons/offBtn_d.png")])
        self.background = AnimatedImage(self.window, (0, 0), listPathImageMenuScreen, 1500)
        self.logo = AnimatedImage(self.window, (400, 120), listPathImageLogo, 1500)
        self.inputData = None

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
            self.screenManager.onlineMode('26.253.176.29')
        if self.offBtn.handleEvent(event):
            self.screenManager.offlineMode()
            self.onlBtn.disable()
            self.offBtn.disable()
            self.exitBtn.disable()
            self.screenManager.changeScreen(PrepareScreen(self.screenManager, self.window))
        if self.inputData is not None:
            res = self.inputData.handleEvent(event) 
            if res[0] == -1:
                self.onlBtn.enable()
                self.offBtn.enable()
                self.exitBtn.enable()
                self.inputData = None
            elif res[0] == 1:
                self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
                self.screenManager.onlineMode(res[1])
                    
    def draw(self):
        self.background.draw()
        self.logo.draw()
        self.onlBtn.draw()
        self.offBtn.draw()
        self.exitBtn.draw()
        if self.inputData is not None:
            self.inputData.draw()
        super().draw()

class FindingScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.createBtn = AnimatedButton(self.window, (600, 300), [resource_path("assets/images/buttons/createBtn_u.png")], [resource_path("assets/images/buttons/createBtn_d.png")])
        self.joinBtn = AnimatedButton(self.window, (650, 400), [resource_path("assets/images/buttons/joinBtn_u.png")], [resource_path("assets/images/buttons/joinBtn_d.png")])
        self.backBtn = AnimatedButton(self.window, (650, 500), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_5.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerFindingScreen]
        
    def handleEvent(self, event):
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(MenuScreen(self.screenManager, self.window))
            self.screenManager.game = None
        if self.createBtn.handleEvent(event):
            self.screenManager.game.signalSend.type = "CREATE_ROOM"
            self.screenManager.game.isRun = True
            self.screenManager.game.start()
            self.screenManager.changeScreen(CreateRoom(self.screenManager, self.window, self.screenManager.game.createRoom()))
        if self.joinBtn.handleEvent(event):
            self.screenManager.game.signalSend.type = "JOIN_ROOM"
            self.screenManager.game.isRun = True
            self.screenManager.game.start()
            self.screenManager.changeScreen(JoinRoom(self.screenManager, self.window))
            
    def draw(self):
        self.background.draw()
        self.createBtn.draw()
        self.joinBtn.draw()
        self.backBtn.draw()
        super().draw()

class CreateRoom(Screen):
    def __init__(self, screenManager, window, roomID):
        super().__init__(screenManager, window)
        self.roomIDText = CustomText(window, (622, 365), roomID, resource_path("fonts/PressStart2P-Regular.ttf"), font_size=50, color=(0, 0, 0))
        self.backBtn = AnimatedButton(self.window, (650, 475), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_4.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerCreateRoomScreen]

    def handleEvent(self, event):
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game.reset()

    def draw(self):
        self.background.draw()
        self.roomIDText.draw()
        self.backBtn.draw()
        super().draw()

class JoinRoom(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.roomIDInput = pygwidgets.InputText(self.window, (630, 365), fontSize=75, width=240)
        self.backBtn = AnimatedButton(self.window, (490, 470), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])
        self.enterBtn = AnimatedButton(self.window, (800, 470), [resource_path("assets/images/buttons/enterBtn_u.png")], [resource_path("assets/images/buttons/enterBtn_d.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_3.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerJoinRoomScreen]

    def handleEvent(self, event):
        self.roomIDInput.handleEvent(event)
        if self.enterBtn.handleEvent(event):
            self.screenManager.game.signalSend.roomID = self.roomIDInput.getValue()
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game.reset()

    def draw(self):
        self.background.draw()
        self.backBtn.draw()
        self.roomIDInput.draw()
        self.enterBtn.draw()
        super().draw()
        

class PrepareScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.readyBtn = AnimatedButton(self.window, (1133, 700), [resource_path("assets/images/buttons/readyBtn_u.png")], [resource_path("assets/images/buttons/readyBtn_d.png")], [resource_path("assets/images/buttons/readyBtn_dis.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerPrepareScreen]

    def handleEvent(self, event):
        if self.readyBtn.handleEvent(event):
            self.readyBtn.disable()
            self.screenManager.game.ready()
    
    def draw(self):
        self.background.draw()
        self.field.draw()
        self.readyBtn.draw()
        self.screenManager.game.player.draw()
        super().draw()


class MyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.switchModeBtn = AnimatedButton(self.window, (1073, 83), [resource_path("assets/images/buttons/switchModeBtn_u.png")], [resource_path("assets/images/buttons/switchModeBtn_d.png")])
        self.torpedoMode = AnimatedImage(self.window, (1073, 83), [resource_path("assets/images/banner/image_6.png")])
        self.radarMode = AnimatedImage(self.window, (1073, 83), [resource_path("assets/images/banner/image_7.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerMyTurnScreen]

    def handleEvent(self, event):
        if self.switchModeBtn.handleEvent(event):
            if self.screenManager.game.player.haveRadar > 0:
                self.screenManager.game.player.switchMode()
                
    def drawTimer(self):
        for i in range(11):
            pygame.draw.rect(self.window, WHITE, (FIELD_COORD[0] + i * CELL_SIZE[0], FIELD_COORD[1], 3, int(FIELD_HEIGHT * (time.time() - self.screenManager.game.timer)/TIME_EACH_TURN)))

        for i in range(int(10 * (time.time() - self.screenManager.game.timer)/TIME_EACH_TURN) + 1):
            pygame.draw.rect(self.window, WHITE, (FIELD_COORD[0], FIELD_COORD[1] + i * CELL_SIZE[1], FIELD_WIDTH, 3))

    def draw(self):
        self.background.draw()
        self.field.draw()      
        self.drawTimer()
        self.screenManager.game.player.draw(True)
        if self.screenManager.game.player.mode == 0:
            self.torpedoMode.draw()
        else:
            self.radarMode.draw()
        super().draw()

class EnemyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.switchModeBtn = AnimatedButton(self.window, (1073, 83), [resource_path("assets/images/buttons/switchModeBtn_u.png")], [resource_path("assets/images/buttons/switchModeBtn_d.png")])
        self.torpedoMode = AnimatedImage(self.window, (1073, 83), [resource_path("assets/images/banner/image_6.png")])
        self.radarMode = AnimatedImage(self.window, (1073, 83), [resource_path("assets/images/banner/image_7.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerEnemyTurnScreen]

    def handleEvent(self, event):
        if self.switchModeBtn.handleEvent(event):
            if self.screenManager.game.player.haveRadar > 0:
                self.screenManager.game.player.switchMode()

    def drawTimer(self):
        for i in range(11):
            pygame.draw.rect(self.window, WHITE, (FIELD_COORD[0] + i * CELL_SIZE[0], FIELD_COORD[1], 3, int(FIELD_HEIGHT * (1 - (time.time() - self.screenManager.game.timer)/TIME_EACH_TURN))))

        for i in range(int(10 * (1 - (time.time() - self.screenManager.game.timer)/TIME_EACH_TURN)) + 1):
            pygame.draw.rect(self.window, WHITE, (FIELD_COORD[0], FIELD_COORD[1] + i * CELL_SIZE[1], FIELD_WIDTH, 3))

    def draw(self):
        self.background.draw()
        self.field.draw()
        self.drawTimer()
        self.screenManager.game.bot.draw(True)
        self.screenManager.game.player.draw(False)
        if self.screenManager.game.player.mode == 0:
            self.torpedoMode.draw()
        else:
            self.radarMode.draw()
        super().draw()
    

class EndScreen(Screen):
    def __init__(self, screenManager, window, isWin): 
        super().__init__(screenManager, window)
        self.banner = CustomText(self.window, (0, 0), str(isWin), resource_path("fonts/PressStart2P-Regular.ttf"), 30, (255, 255, 255))
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])
        self.banner = [AnimatedImage(self.window, loc, listPath) for loc, listPath in listPathImageBannerEndScreen]
        self.backBtn = AnimatedButton(self.window, (1183, 700), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])

    def handleEvent(self, event):
        if self.backBtn.handleEvent(event):
            self.screenManager.game.reset()
            self.screenManager.changeScreen(MenuScreen(self.screenManager, self.window))
            self.screenManager.game = None
    
    def draw(self):
        self.background.draw()
        self.field.draw()
        self.screenManager.game.player.drawEnd()
        self.backBtn.draw()
        super().draw()