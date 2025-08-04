import pygame
from pygame.locals import *
from constants import *

class AnimatedImage():
    def __init__(self, window, loc, lstPath, fps=0):
        self.window = window
        self.loc = loc
        self.__indexFrame = 0
        self.__image = [pygame.image.load(path).convert_alpha() for path in lstPath]
        self.fps = fps
        self.totalFrame = len(self.__image)
        self._startTime = pygame.time.get_ticks()

    def draw(self):
        self.window.blit(self.__image[self.__indexFrame], self.loc)
        if pygame.time.get_ticks() - self._startTime >= self.fps and self.fps != 0:
            self._startTime = pygame.time.get_ticks()
            self.__indexFrame = (self.__indexFrame + 1) % self.totalFrame

class AnimatedButton():
    def __init__(self, window, loc, lstImageUp, lstImageDown, fps=0):
        self.window = window
        self.loc = loc
        self.lstImageUp = [pygame.image.load(path).convert_alpha() for path in lstImageUp]
        self.lstImageDown = [pygame.image.load(path).convert_alpha() for path in lstImageDown]
        self.state = 0 # 0: up, 1: down, -1: disarmed
        self.indexImage = 0
        self.__hitBox = self.lstImageUp[self.indexImage].get_rect(topleft=self.loc)
        self._startTime = pygame.time.get_ticks()
        self.fps = fps

    def handleEvent(self, eventObj):
        if eventObj.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return False

        eventPointInButtonRect = self.__hitBox.collidepoint(eventObj.pos)

        if self.state == 0:
            if (eventObj.type == pygame.MOUSEBUTTONDOWN) and eventPointInButtonRect:
                self.state = 1
        elif self.state == 1:
            if (eventObj.type == pygame.MOUSEBUTTONUP) and eventPointInButtonRect:
                self.state = 0
                return True  # clicked!
            if (eventObj.type == pygame.MOUSEMOTION) and (not eventPointInButtonRect):
                self.state = -1
        elif self.state == -1:
            if eventPointInButtonRect:
                self.state = 1
            elif eventObj.type == pygame.MOUSEBUTTONUP:
                self.state = 0

        return False

    def draw(self):
        if self.state == 0:
            self.window.blit(self.lstImageUp[self.indexImage], self.loc)
            if pygame.time.get_ticks() - self._startTime >= self.fps and self.fps != 0:
                self._startTime = pygame.time.get_ticks()
                self.indexImage = (self.indexImage + 1) % len(self.lstImageUp)
        else: 
            self.window.blit(self.lstImageDown[self.indexImage], self.loc)
            if pygame.time.get_ticks() - self._startTime >= self.fps and self.fps != 0:
                self._startTime = pygame.time.get_ticks()
                self.indexImage = (self.indexImage + 1) % len(self.lstImageDown)
        

class CustomText():
    def __init__(self, surface, loc, text, font_path, font_size, color=(0, 0, 0)):
        self.surface = surface
        self.loc = loc
        self.text = text
        self.font = pygame.font.Font(font_path, font_size)
        self.color = color

    def draw(self):
        text_surface = self.font.render(self.text, True, self.color)
        self.surface.blit(text_surface, self.loc)

    def setText(self, newText):
        self.text = newText

    def setLoc(self, newLoc):
        self.loc = newLoc