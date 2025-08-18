from listPath import *
from widget import *
from screen import *
from player import *
from network import *
from bot import *
import random
from mySignal import *
from constants import *
import time
import threading
from radar import *
import pickle

       

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
        self.isConnected = True
        self.timer = time.monotonic()
        
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
                    self.timer = time.monotonic()
                    self.player.canFire = True
                    self.signalSend.type = "WAITING_PL"
                    self.signalSend.data = self.player.lastPosEnemyFire
                    self.signalSend.anotherData = self.player.lastPosEnemyRadar
                
                if self.isConnected:
                    res = self.player.handleEvent(event)
                    if res:
                        self.player.lastPosFire = res
                        self.signalSend.type = "FIRE_TORPEDO" if self.player.mode == 0 else "FIRE_RADAR"
                        soundEffect = self.manager.fireTorpedoSound if self.player.mode == 0 else self.manager.fireRadarSound
                        soundEffect.play()
                        if self.player.mode == 1: 
                            self.player.haveRadar -= 1
                            self.player.mode = 0
                        self.signalSend.data = res
                        self.isRecieveResult = False
                        self.player.coolDown = time.monotonic()

                if self.signalRecieve.type == "WAITING_PL":
                    if time.monotonic() - self.player.coolDown > COOL_DOWN and self.player.canFire == False:
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
                    self.timer = time.monotonic()
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
            