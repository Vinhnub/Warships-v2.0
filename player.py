import pygame
from pygame.locals import *
from constants import *
from listPath import *
from ship import *
from torpedo import *
from radar import *
import time

class Player():
    def __init__(self, window, gameMode=True): #True: onl, False: off
        self.window = window
        self.mode = 0 # o: torpedo, 1: radar
        self.listShip = [Ship(self.window, path[1], path[0], path[2]) for path in (listPathShipOnl if gameMode else listPathShipOff)] 
        self.listEnemyShip = None
        self.__isMouseDown = False
        self.__firstPos = None # pos when player click mouse down to move or ronate ship
        self.__shipSelected = None # the ship player select to move
        self.isReady = False
        self.coolDown = time.time()
        self.listMyTorpedo = []
        self.listEnemyTorpedo = []
        self.myRadar = None
        self.enemyRadar = None
        self.haveRadar = 0
        self.canFire = None
        self.lastPosFire = None
        self.lastPosEnemyFire = None
        self.lastPosEnemyRadar = None
        self.__listPosShip = [[0 for _ in range(10)] for __ in range(10)]

    def switchMode(self):
        self.mode = 1 - self.mode

    def getShipDetail(self):
        listTemp = []
        for ship in self.listShip:
            listTemp.append((ship.loc, ship.direction))
        return listTemp

    def calListEnemyShip(self, data):
        if self.listEnemyShip is not None or data is None: return
        count = 0
        self.listEnemyShip = []
        for item in data:
            if count >= 5: return
            loc, direction = item
            self.listEnemyShip.append(Ship(self.window, loc, listPathShipOnl[count][0], listPathShipOnl[count][2], direction=direction))
            count += 1

    def calListPosShip(self):
        count = 0
        for ship in self.listShip:
            if count >= 5: break
            count += 1
            for x in range(ship.loc[0], ship.loc[0] + ship.width, CELL_SIZE[0]):
                for y in range(ship.loc[1], ship.loc[1] + ship.height, CELL_SIZE[0]):
                    self.__listPosShip[int((x - FIELD_COORD[0])/CELL_SIZE[0])][int((y - FIELD_COORD[1])/CELL_SIZE[1])] = 1
        
        for i in range(count, len(self.listShip)):
            self.__listPosShip[int((self.listShip[i].loc[0] - FIELD_COORD[0])/CELL_SIZE[0])][int((self.listShip[i].loc[1] - FIELD_COORD[1])/CELL_SIZE[1])] = 2

        return self.__listPosShip
    
    def isCorrect(self, pos):
        if pos is None: return False
        return self.__listPosShip[pos[0]][pos[1]]
    
    def numCorrect(self, pos):
        result = 0
        for x in range(max(0, pos[0] - 1), min(10, pos[0] + 2)):
            for y in range(max(0, pos[1] - 1), min(10, pos[1] + 2)):
                if self.__listPosShip == 1:
                    result += 1
        return result
    
    def handleEvent(self, event):
        if (not self.isReady):
            self.moveShip(event)
        if self.canFire:
            res = self.fire(event)
            if res:
                self.canFire = False
            return res
        return False

    def fire(self, event):
        if event is None: return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            firePos = pygame.mouse.get_pos()
            if FIELD_COORD[0] < firePos[0] and firePos[0] < FIELD_COORD[0] + FIELD_WIDTH and FIELD_COORD[1] < firePos[1] and firePos[1] < FIELD_COORD[1] + FIELD_HEIGHT:
                if self.mode == 0:
                    for oTorpedo in self.listMyTorpedo:
                        if oTorpedo.getHitBox().collidepoint(firePos):
                            return False
                return (int((firePos[0] - FIELD_COORD[0])/CELL_SIZE[0]), int((firePos[1] - FIELD_COORD[1])/CELL_SIZE[1]))
        return False
    
    def drawEnd(self):
        if self.listEnemyShip is not None:
            for ship in self.listEnemyShip:
                ship.draw()
        for oTorpedo in self.listMyTorpedo:
            oTorpedo.draw()

    def draw(self, isMyTurn=None):
        if isMyTurn is None:
            for ship in self.listShip:
                ship.draw()
        if isMyTurn:
            for oTorpedo in self.listMyTorpedo:
                if not oTorpedo.drawAnimation():
                    oTorpedo.draw()
            if self.myRadar is not None:
                self.myRadar.drawAnimation()
        else:
            for ship in self.listShip:
                ship.draw()
            for oTorpedo in self.listEnemyTorpedo:
                if not oTorpedo.drawAnimation():
                    oTorpedo.draw()
            if self.enemyRadar is not None:
                self.enemyRadar.drawAnimation()
        
    def moveShip(self, event):
        if event is None: return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.__firstPos = pygame.mouse.get_pos()
            for ship in self.listShip:
                if ship.getHitBox().collidepoint(self.__firstPos):
                    ship.rotate(True)
                    if ship.isCollideAnotherShip(self.listShip) or ship.isOutOfField():
                        ship.rotate(False)
                    else:
                        ship.updateNewLoc()
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.__firstPos = pygame.mouse.get_pos()
            for ship in self.listShip:
                if ship.getHitBox().collidepoint(self.__firstPos):
                    self.__shipSelected = ship
                    self.__isMouseDown = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.__isMouseDown == True:
            if self.__shipSelected.isCollideAnotherShip(self.listShip) or self.__shipSelected.isOutOfField():
                self.__shipSelected.loc = self.__shipSelected.oldLoc
                self.__shipSelected.updateHitBox()
            else:
                self.__shipSelected.updateNewLoc()
            self.__isMouseDown = False
        
        if self.__isMouseDown:  
            if event.type == MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
                self.__shipSelected.updatePos(self.__firstPos, mousePos)


            