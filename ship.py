from constants import *
import pygame
from torpedo import *

class Ship():
    def __init__(self, window, loc, path, id):
        self.window = window
        self.oldLoc = loc
        self.loc = loc
        self.id = id
        self.__image = pygame.image.load(path).convert_alpha()
        self.width = self.__image.get_rect().width
        self.height = self.__image.get_rect().height
        self.__hitBox = pygame.Rect(self.loc[0], self.loc[1], self.width, self.height)
        self.__direction = 0 # 0: down, 1: right, 2: up, 3:left

    def getHitBox(self):
        return self.__hitBox
    
    def updateHitBox(self):
        self.__hitBox = pygame.Rect(self.loc[0], self.loc[1], self.__image.get_rect().width, self.__image.get_rect().height)
    
    def rotate(self, leftOrRight): # True: right, False: left
        if leftOrRight:
            self.__direction = (self.__direction + 1) % len(MATRIX_ROTATE_RIGHT)
            self.__image = pygame.transform.rotate(self.__image, 90)
            self.loc = (self.loc[0] - MATRIX_ROTATE_RIGHT[self.__direction][0]*(self.height - self.width), self.loc[1] + MATRIX_ROTATE_RIGHT[self.__direction][1]*(self.height - self.width))
            self.width, self.height = self.height, self.width
            self.updateHitBox()
        else:
            if self.__direction - 1 < 0: self.__direction = len(MATRIX_ROTATE_LEFT) - 1
            else: self.__direction -= 1
            self.__image = pygame.transform.rotate(self.__image, 270)
            self.loc = (self.loc[0] - MATRIX_ROTATE_LEFT[self.__direction][0]*(self.height - self.width), self.loc[1] + MATRIX_ROTATE_LEFT[self.__direction][1]*(self.height - self.width))
            self.width, self.height = self.height, self.width
            self.updateHitBox()

    def draw(self, window):
        window.blit(self.__image, self.loc)

    def updatePos(self, mousePosOld, mousePosNew):
        self.loc = (self.oldLoc[0] + int((mousePosNew[0] - mousePosOld[0])/CELL_SIZE[0]) * CELL_SIZE[0], self.oldLoc[1] + int((mousePosNew[1] - mousePosOld[1])/CELL_SIZE[0]) * CELL_SIZE[0])
        self.updateHitBox()

    def isOutOfField(self):
        if (self.loc[1] < FIELD_COORD[1]) or (self.loc[1] + self.height > FIELD_COORD[1] + FIELD_HEIGHT) or (self.loc[0] < FIELD_COORD[0]) or (self.loc[0] + self.width > FIELD_COORD[0] + FIELD_WIDTH):
            return True
        return False

    def isCollideAnotherShip(self, anotherShips):
        for ship in anotherShips:
            if (self.__hitBox.colliderect(ship.getHitBox()) and self.id != ship.id):
                return True
        return False

    def updateNewLoc(self):
        self.oldLoc = self.loc
    
    