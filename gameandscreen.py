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
import time
import threading
from radar import *
import pickle

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


class CreateRoom(Screen):
    def __init__(self, screenManager, window, roomID):
        super().__init__(screenManager, window)
        self.roomIDText = CustomText(window, (500, 350), roomID, resource_path("fonts/PressStart2P-Regular.ttf"), font_size=50, color=(255, 255, 255))
        self.backBtn = AnimatedButton(self.window, (550, 450), [resource_path("assets/images/buttons/backBtn_u.png")], [resource_path("assets/images/buttons/backBtn_d.png")])

    def handleEvent(self, event):
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game.reset()

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
            self.screenManager.game.signalSend.roomID = self.roomIDInput.getValue()
        if self.backBtn.handleEvent(event):
            self.screenManager.changeScreen(FindingScreen(self.screenManager, self.window))
            self.screenManager.game.reset()

    def draw(self):
        self.backBtn.draw()
        self.roomIDInput.draw()
        self.enterBtn.draw()
        

class PrepareScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.readyBtn = AnimatedButton(self.window, (500, 700), [resource_path("assets/images/buttons/readyBtn_u.png")], [resource_path("assets/images/buttons/readyBtn_d.png")], [resource_path("assets/images/buttons/readyBtn_dis.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])

    def handleEvent(self, event):
        if self.readyBtn.handleEvent(event):
            self.readyBtn.disable()
            self.screenManager.game.ready()
    
    def draw(self):
        self.background.draw()
        self.field.draw()
        self.readyBtn.draw()
        self.screenManager.game.player.draw()

class MyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.timer = CustomText(self.window, (0, 0), "", resource_path("fonts/PressStart2P-Regular.ttf"), 30, (255, 255, 255))
        self.switchModeBtn = AnimatedButton(self.window, (0, 700), [resource_path("assets/images/buttons/switchModeBtn_u.png")], [resource_path("assets/images/buttons/switchModeBtn_d.png")])
        self.torpedoMode = AnimatedImage(self.window, (0, 600), [resource_path("assets/images/torpedoMode.png")])
        self.radarMode = AnimatedImage(self.window, (0, 600), [resource_path("assets/images/radarMode.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])

    def handleEvent(self, event):
        if self.switchModeBtn.handleEvent(event):
            if self.screenManager.game.player.haveRadar > 0:
                self.screenManager.game.player.switchMode()

    def draw(self):
        self.background.draw()
        self.field.draw()
        self.screenManager.game.player.draw(True)
        self.timer.draw()
        self.switchModeBtn.draw()
        if self.screenManager.game.player.mode == 0:
            self.torpedoMode.draw()
        else:
            self.radarMode.draw()

class EnemyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.timer = CustomText(self.window, (0, 0), "", resource_path("fonts/PressStart2P-Regular.ttf"), 30, (255, 255, 255))
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])

    def handleEvent(self, event):
        pass

    def draw(self):
        self.background.draw()
        self.field.draw()
        self.screenManager.game.player.draw(False)
        self.timer.draw()

class EndScreen(Screen):
    def __init__(self, screenManager, window, isWin): 
        super().__init__(screenManager, window)
        self.banner = CustomText(self.window, (0, 0), str(isWin), resource_path("fonts/PressStart2P-Regular.ttf"), 30, (255, 255, 255))
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.background = AnimatedImage(self.window, (0, 0), [resource_path("assets/images/background/image_2.png")])

    def handleEvent(self, event):
        pass
    
    def draw(self):
        self.background.draw()
        self.banner.draw()
        self.field.draw()
        self.screenManager.game.player.drawEnd()

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
        self.signalSend = SignalSended()
        self.signalRecieve = SignalRecieved()
        self.isRun = False
        self.sendLock = threading.Lock()
        self.isRecieveResult = False
        
    def reset(self):
        self.isRun = False
        self.signalSend = SignalSended()
        self.signalRecieve = SignalRecieved()
        self.player = Player(self.manager.window)
    
    def start(self):
        threading.Thread(target=self.updSender, daemon=True).start()
        threading.Thread(target=self.udpReciever, daemon=True).start()

    def createRoom(self):
        self.signalSend.roomID = str(random.randint(10000, 99999))
        return self.signalSend.roomID
    
    def ready(self):
        self.signalSend.type = "READY"
        self.signalSend.data = self.player.calListPosShip()
        self.player.isReady = True

    def updSender(self):
        while self.isRun:
            time.sleep(0.05)
            with self.sendLock:
                packet = pickle.dumps(self.signalSend)
            try:
                self.network.client.sendto(packet, self.network.addr)
            except Exception as e:
                print("[ERROR] Lỗi khi gửi dữ liệu:", e)
            

    def udpReciever(self):
        while self.isRun:
            try:
                data, addr = self.network.client.recvfrom(4096)
                self.signalRecieve = pickle.loads(data)
            except Exception as e:
                print("[ERROR] Lỗi khi nhận dữ liệu:", e)
        

    def running(self, event=None):
        if not self.isRun:
            return

        if self.signalSend.type is None or self.signalSend.roomID is None or self.signalSend.roomID == "":
            return
        
        if self.signalRecieve.phase == "PREPARE":
            if not isinstance(self.manager.currentScreen, PrepareScreen):
                self.manager.changeScreen(PrepareScreen(self.manager, self.manager.window))
                self.signalSend.type = "WAITING_PR"
                self.signalSend.data = None
            self.player.handleEvent(event)

        if self.signalRecieve.phase == "PLAYING":
            if self.signalRecieve.turnIP == self.signalRecieve.playerIP:
                if not isinstance(self.manager.currentScreen, MyTurnScreen):
                    self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))
                    self.player.canFire = True
                    self.signalSend.type = "WAITING_PL"
                    self.signalSend.data = len(self.player.listEnemyTorpedo)
                    self.signalSend.anotherData = self.player.lastPosEnemyRadar
                
                res = self.player.handleEvent(event)
                if res:
                    self.player.lastPosFire = res
                    self.signalSend.type = "FIRE_TORPEDO" if self.player.mode == 0 else "FIRE_RADAR"
                    if self.player.mode == 1: 
                        self.player.haveRadar -= 1
                        self.player.mode = 0
                    self.signalSend.data = res
                    self.isRecieveResult = False
                    self.player.coolDown = time.time()

                if self.signalRecieve.type == "WAITING_PL":
                    self.manager.currentScreen.timer.setText(str(int(self.signalRecieve.data)))
                    if time.time() - self.player.coolDown > COOL_DOWN and self.player.canFire == False:
                        self.player.canFire = True

                if self.signalRecieve.type == "FIRE_TORPEDO_RESULT":
                    if not self.isRecieveResult:
                        self.isRecieveResult = True
                        self.player.listMyTorpedo.append(Torpedo(self.manager.window, self.player.lastPosFire, listPathTopedoA, pathImageTorpedo, self.signalRecieve.data, 100))
                        self.signalSend.type = "WAITING_PL"
                        self.signalSend.data = len(self.player.listEnemyTorpedo)
                        self.signalSend.anotherData = self.player.lastPosEnemyRadar
                        if self.signalRecieve.data == 2:
                            self.player.haveRadar += 1

                if self.signalRecieve.type == "FIRE_RADAR_RESULT":
                    self.player.myRadar.append((Radar(self.manager.window, self.player.lastPosFire, listPathRadarA, self.signalRecieve.data, 100), self.player.lastPosFire))
                    self.signalSend.type = "WAITING_PL"
                    self.signalSend.data = len(self.player.listEnemyTorpedo)
                    self.signalSend.anotherData = self.player.lastPosEnemyRadar

            else:
                if not isinstance(self.manager.currentScreen, EnemyTurnScreen):
                    self.manager.changeScreen(EnemyTurnScreen(self.manager, self.manager.window))
                    self.signalSend.type = "WAITING_PL"
    
                self.signalSend.data = self.player.lastPosEnemyFire
                self.signalSend.anotherData = self.player.lastPosEnemyRadar

                if self.signalRecieve.type == "WAITING_PL":
                    self.manager.currentScreen.timer.setText(str(int(self.signalRecieve.data)))
                
                if self.signalRecieve.type == "ENEMY_FIRE_TORPEDO":
                    if self.player.lastPosEnemyFire != self.signalRecieve.data:
                        self.player.lastPosEnemyFire = self.signalRecieve.data
                        self.player.listEnemyTorpedo.append(Torpedo(self.manager.window, self.signalRecieve.data, listPathTopedoA, pathImageTorpedo, self.player.isCorrect(self.signalRecieve.data), 100))

                if self.signalRecieve.type == "ENEMY_FIRE_RADAR":
                    if self.player.lastPosEnemyRadar != self.signalRecieve.data:
                        self.player.lastPosEnemyRadar = self.signalRecieve.data
                        self.player.enemyRadar.append((Radar(self.manager.window, self.player.lastPosEnemyRadar, listPathRadarA, self.player.numCorrect(self.player.lastPosEnemyRadar), 100), self.player.lastPosEnemyRadar))

        if self.signalRecieve.phase == "END":
            if not isinstance(self.manager.currentScreen, EndScreen):
                self.manager.changeScreen(EndScreen(self.manager, self.manager.window, self.signalRecieve.data))
                self.signalSend.data = self.player.getShipDetail()
                self.signalSend.type = "MY_SHIP"

            if self.signalRecieve.type == "ENEMY_SHIP":
                if self.signalRecieve.data is not None:
                    self.player.calListEnemyShip(self.signalRecieve.data)
                    self.signalSend.type = None
                    self.signalSend.data = None
            