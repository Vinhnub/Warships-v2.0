from listPath import *
from widget import *
from abc import abstractmethod
from player import *
from network import *
import pygwidgets
from botLogic import *
from botPlayer import *
import random
from mySignal import *
from constants import *
import time
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
            self.onlBtn.disable()
            self.offBtn.disable()
            self.exitBtn.disable()
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

    def handleEvent(self, event):
        pass

    def draw(self):
        self.field.draw()
        self.screenManager.game.player.draw(self.window, True)

class EnemyTurnScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        
    def handleEvent(self, event):
        pass

    def draw(self):
        self.field.draw()
        self.screenManager.game.player.draw(self.window, False)

class WINTemporaryEndScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.win = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/textWIN.png")])
    def handleEvent(self):
        pass
    def draw(self):
        self.field.draw()
        self.win.draw()

class LOSETemporaryEndScreen(Screen):
    def __init__(self, screenManager, window):
        super().__init__(screenManager, window)
        self.field = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/field.png")])
        self.lose = AnimatedImage(self.window, FIELD_COORD, [resource_path("assets/images/textLOSE.png")])
    def handleEvent(self):
        pass
    def draw(self):
        self.field.draw()
        self.lose.draw()   
        

# ============================================================ MODE ============================================================
class OfflineMode:
    def __init__(self, manager):
        self.manager = manager
        self.player = Player(manager.window)
        self.phase = "PREPARE"
        self.turn = "player"
        self.bot = None

        self.delay_start_time = None
        self.delayTime = 800  # ms
        self.waiting_for_bot = False

        self.animation_end_time = 0
        self.player_pending_hit = None  # Kết quả animation người chơi
        self.bot_pending_hit = None     # Kết quả animation bot
        
        self.countBotHitTrue = 0
        self.countPlayerHitTrue = 0
        
        self.timeEndTurn = None
        self.TIME_EACH_TURN = TIME_EACH_TURN // 1000
    def running(self, event=None):
        if event:
            self.handle_event(event)
        self.update()

    def handle_event(self, event):
        if self.phase == "PREPARE":
            if not isinstance(self.manager.currentScreen, PrepareScreen):
                self.manager.changeScreen(PrepareScreen(self.manager, self.manager.window))
            self.player.handleEvent(event)

        elif self.phase == "PLAYING":
            if self.turn == "player":
                self.player.canFire = True
                if not isinstance(self.manager.currentScreen, MyTurnScreen):
                    self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))
                    self.timeEndTurn = time.time() + self.TIME_EACH_TURN
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.player.handleEvent(event)
                    print(f"player: {pos}")
                    if pos:
                        hit = self.bot.isCorrect(pos)
                        if hit:
                           self.countPlayerHitTrue += 1
                           print(self.countPlayerHitTrue)
                           if self.countPlayerHitTrue == 17:
                              self.manager.changeScreen(WINTemporaryEndScreen(self.manager, self.manager.window))
                        pixel_loc = (
                            FIELD_COORD[0] + pos[0] * CELL_SIZE[0] + 3,
                            FIELD_COORD[1] + pos[1] * CELL_SIZE[1] + 3
                        )
                        torpedo = Torpedo(self.player.window, pixel_loc, listPathTopedoA, pathImageTorpedo, hit, spf=50)
                        self.player.listMyTorpedo.append(torpedo)

                        self.animation_end_time = time.time() + 1.2 
                        self.player_pending_hit = hit
                        self.timeEndTurn = "End"

    def update(self):
        if self.phase != "PLAYING":
            return
        if isinstance(self.manager.currentScreen, (WINTemporaryEndScreen, LOSETemporaryEndScreen)):
           return
        now = time.time()
        if self.turn == "player" and self.timeEndTurn == "End":
           self.timeEndTurn = time.time() + 1.5
        if self.turn == "player" and now >= self.timeEndTurn:
            print("Player didn't shoot , switching to bot's turn")
            self.manager.changeScreen(EnemyTurnScreen(self.manager, self.manager.window))
            self.turn = "bot"
            self.waiting_for_bot = True
            self.delay_start_time = pygame.time.get_ticks()       
        else:
            # Xử lý animation người chơi
            if self.timeEndTurn - now >= 0:
                print(self.timeEndTurn - now)
            if self.turn == "player" and self.player_pending_hit is not None:
                if now >= self.animation_end_time:
                    if not self.player_pending_hit:
                        print("Player missed, switching to bot's turn")
                        self.turn = "bot"
                        self.waiting_for_bot = True
                        self.delay_start_time = pygame.time.get_ticks()
                        self.manager.changeScreen(EnemyTurnScreen(self.manager, self.manager.window))
                    else:
                        print("Player hit, continues turn")
                        self.timeStartTurn = pygame.time.get_ticks()
                        self.turn = "player"
                        self.timeEndTurn = time.time() + self.TIME_EACH_TURN
                        self.waiting_for_bot = False
                    self.player_pending_hit = None

            #animation bot
            if self.timeEndTurn - now <= 0:
                if self.turn == "bot" and self.bot_pending_hit is not None:
                    if now >= self.animation_end_time:
                        if not self.bot_pending_hit:
                            print("Bot missed, switching to player's turn")
                            self.turn = "player"
                            self.timeEndTurn = time.time() + self.TIME_EACH_TURN
                            self.waiting_for_bot = False
                            self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))
                        else:
                            print("Bot hit, continues turn")
                            self.turn = "bot"
                            self.countBotHitTrue += 1
                            if self.countBotHitTrue == 17:
                               self.manager.changeScreen(LOSETemporaryEndScreen(self.manager, self.manager.window))
                            self.waiting_for_bot = True
                            self.delay_start_time = pygame.time.get_ticks()
                        self.bot_pending_hit = None
            else:
                return

            # BOT logic
            if self.turn == "bot" and self.waiting_for_bot:
                now_ticks = pygame.time.get_ticks()
                if now_ticks - self.delay_start_time >= self.delayTime and self.bot_pending_hit is None:
                    self.waiting_for_bot = False
                    hit = self.bot.makeHit()
                    self.animation_end_time = time.time() + 1.2
                    self.bot_pending_hit = hit

    def draw(self):
        if self.turn == "player":
            self.player.draw(self.manager.window, isMyTurn=True)
        elif self.turn == "bot":
            self.bot.draw(self.manager.window, isMyTurn=True)

    def ready(self):
        self.player.isReady = True
        self.player.calListPosShip()
        self.bot = PlayerAI(self.manager.window, self.player)
        self.bot.auto_place_ships()
        self.bot.isReady = True
        self.phase = "PLAYING"
        self.turn = "player"
        print(f"Phase set to: {self.phase}, Turn set to: {self.turn}")
        self.player_pending_hit = None
        self.bot_pending_hit = None
        self.animation_end_time = 0
        self.waiting_for_bot = False
        self.delay_start_time = None
        self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))
        self.countBotHitTrue = 0
        self.countPlayerHitTrue = 0
        self.timeEndTurn = time.time() + self.TIME_EACH_TURN
        self.TIME_EACH_TURN = TIME_EACH_TURN // 1000


class OnlineMode():
    def __init__(self, manager, serverIP):
        self.manager = manager
        self.player = Player(manager.window)
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

    def running(self, event):
        if self.type is None or self.roomID is None or self.roomID == "":
            return
        newSignal = SignalSended(self.type, self.roomID, self.data)
        respon = self.network.send(newSignal)
        if respon.phase == "PREPARE":
            if not isinstance(self.manager.currentScreen, PrepareScreen):
                self.manager.changeScreen(PrepareScreen(self.manager, self.manager.window))
            self.type = "WAITING"
            self.player.handleEvent(event)

        if respon.phase == "PLAYING":
            if respon.turnIP == respon.playerIP:
                if not isinstance(self.manager.currentScreen, MyTurnScreen):
                    self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))

            else:
                if not isinstance(self.manager.currentScreen, EnemyTurnScreen):
                    self.manager.changeScreen(EnemyTurnScreen(self.manager, self.manager.window))

    def draw(self):
        pass
