from listPath import *
from widget import *
from screen import *
from player import *
from network import *
from botLogic import *
from botPlayer import *
import random
from mySignal import *
from constants import *
import time
import threading
from radar import *
import pickle

       

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
        self.timer = None
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.player.handleEvent(event)
                    print(f"player: {pos}")
                    if pos:
                        hit = self.bot.isCorrect(pos)
                        pixel_loc = (
                            FIELD_COORD[0] + pos[0] * CELL_SIZE[0] + 3,
                            FIELD_COORD[1] + pos[1] * CELL_SIZE[1] + 3
                        )
                        torpedo = Torpedo(self.player.window, pixel_loc, listPathTopedoA, pathImageTorpedo, hit, spf=50)
                        self.player.listMyTorpedo.append(torpedo)

                        self.animation_end_time = time.time() + 1.2 
                        self.player_pending_hit = hit

    def update(self):
        if self.phase != "PLAYING":
            return
        now = time.time()
        # Xử lý animation người chơi
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
                    self.countPlayerHitTrue += 1
                    if self.countPlayerHitTrue == 17:
                        self.manager.changeScreen(EndScreen(self.manager, self.manager.window))
                    self.turn = "player"
                    self.waiting_for_bot = False
                self.player_pending_hit = None

        #animation bot
        if self.turn == "bot" and self.bot_pending_hit is not None:
            if now >= self.animation_end_time:
                if not self.bot_pending_hit:
                    print("Bot missed, switching to player's turn")
                    self.turn = "player"
                    self.waiting_for_bot = False
                    self.manager.changeScreen(MyTurnScreen(self.manager, self.manager.window))
                else:
                    print("Bot hit, continues turn")
                    self.turn = "bot"
                    self.countBotHitTrue += 1
                    if self.countBotHitTrue == 17:
                       self.manager.changeScreen(EndScreen(self.manager, self.manager.window))
                    self.waiting_for_bot = True
                    self.delay_start_time = pygame.time.get_ticks()
                self.bot_pending_hit = None

        # BOT logic
        if self.turn == "bot" and self.waiting_for_bot:
            now_ticks = pygame.time.get_ticks()
            if now_ticks - self.delay_start_time >= self.delayTime and self.bot_pending_hit is None:
                self.waiting_for_bot = False
                hit = self.bot.makeHit()
                self.animation_end_time = time.time() + 1.2
                self.bot_pending_hit = hit
                self.timer = time.time()
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
        self.timer = time.time()




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
        self.isConnected = True
        self.timer = time.time()
        
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
                self.isConnected = True
            except Exception as e:
                self.manager.currentScreen.warning = Warning(self.manager.window, (80, 370), "Lost connection from server", 100)
                self.isConnected = False
        

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
                    self.timer = time.time()
                    self.player.canFire = True
                    self.signalSend.type = "WAITING_PL"
                    self.signalSend.data = self.player.lastPosEnemyFire
                    self.signalSend.anotherData = self.player.lastPosEnemyRadar
                
                if self.isConnected:
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
                    if time.time() - self.player.coolDown > COOL_DOWN and self.player.canFire == False:
                        self.player.canFire = True

                if self.signalRecieve.type == "FIRE_TORPEDO_RESULT":
                    if not self.isRecieveResult:
                        self.isRecieveResult = True
                        self.player.listMyTorpedo.append(Torpedo(self.manager.window, self.player.lastPosFire, listPathTopedoA, pathImageTorpedo, self.signalRecieve.data, 100))
                        self.signalSend.type = "WAITING_PL"
                        self.signalSend.data = self.player.lastPosEnemyFire
                        self.signalSend.anotherData = self.player.lastPosEnemyRadar
                        if self.signalRecieve.data == 2:
                            self.player.haveRadar += 1

                if self.signalRecieve.type == "FIRE_RADAR_RESULT":
                    self.player.myRadar.append((Radar(self.manager.window, self.player.lastPosFire, listPathRadarA, self.signalRecieve.data, 100), self.player.lastPosFire))
                    self.signalSend.type = "WAITING_PL"
                    self.signalSend.data = self.player.lastPosEnemyFire
                    self.signalSend.anotherData = self.player.lastPosEnemyRadar

            else:
                if not isinstance(self.manager.currentScreen, EnemyTurnScreen):
                    self.manager.changeScreen(EnemyTurnScreen(self.manager, self.manager.window))
                    self.timer = time.time()
                    self.signalSend.type = "WAITING_PL"
    
                self.signalSend.data = self.player.lastPosEnemyFire
                self.signalSend.anotherData = self.player.lastPosEnemyRadar

                if self.signalRecieve.type == "WAITING_PL":
                    pass
                
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
            