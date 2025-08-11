from constants import *
from listPath import *
import pygame

class Radar():
    def __init__(self, window, loc, listRadarA, numCorrect, spf=0): # spf: Time to display 1 image
        self.window = window
        self.loc = (FIELD_COORD[0] + (loc[0] - 1) * CELL_SIZE[0] + 3, FIELD_COORD[1] + (loc[1] - 1) * CELL_SIZE[1] + 3)
        self.__listImageAnimation = [pygame.image.load(path).convert_alpha() for path in listRadarA] + [pygame.image.load("assets/images/radar_frames/result_"+str(numCorrect)+".png").convert_alpha()]
        self.__spf = spf # seconds per frame
        self.__startTime = pygame.time.get_ticks()
        self.__index = 0

    def drawAnimation(self):
        if self.__index == len(self.__listImageAnimation): return False
        self.window.blit(self.__listImageAnimation[self.__index], self.loc)
        if pygame.time.get_ticks() - self.__startTime > self.__spf:
            self.__startTime = pygame.time.get_ticks()
            self.__index += 1
        return True
