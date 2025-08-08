from constants import *
from listPath import *
import pygame

class Torpedo():
    def __init__(self, window, loc, listPathTopedoA, pathImages, isHitTheTarget, spf=0): # spf: Time to display 1 image
        self.window = window
        self.loc = (FIELD_COORD[0] + int((loc[0] - FIELD_COORD[0])/CELL_SIZE[0])*CELL_SIZE[0] + 3, FIELD_COORD[1] + int((loc[1] - FIELD_COORD[1])/CELL_SIZE[1])*CELL_SIZE[1] + 3)
        self.__listImageAnimation = [pygame.image.load(path).convert_alpha() for path in listPathTopedoA]
        self.__spf = spf # seconds per frame
        self.__image = pygame.image.load(pathImages[0]).convert_alpha() if isHitTheTarget else pygame.image.load(pathImages[1]).convert_alpha()
        self.__startTime = pygame.time.get_ticks()
        self.__index = 0
        self.__hitBox = pygame.Rect(self.loc[0], self.loc[1], self.__image.get_rect().width, self.__image.get_rect().height)

    def getHitBox(self):
        return self.__hitBox

    def drawAnimation(self):
        if self.__index == len(self.__listImageAnimation): return False
        self.window.blit(self.__listImageAnimation[self.__index], self.loc)
        if pygame.time.get_ticks() - self.__startTime > self.__spf:
            self.__startTime = pygame.time.get_ticks()
            self.__index += 1
        return True

    def draw(self):
        self.window.blit(self.__image, self.loc)