import pygame
from pygame.locals import *
import pygwidgets
from constants import *

import pygwidgets
import os
from listPath import *

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
        self.state = 0 # 0: up, 1: down, -1: disarmed, 2: disable
        self.indexImage = 0
        self.__hitBox = self.lstImageUp[self.indexImage].get_rect(topleft=self.loc)
        self._startTime = pygame.time.get_ticks()
        self.fps = fps

    def disable(self):
        self.state = 2

    def enable(self):
        self.state = 0

    def handleEvent(self, eventObj):
        if self.state == 2:
            return False

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
        if self.state == 0 or self.state == 2:
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

class Warning:
   def __init__(self, window, loc, duration=5000):
        self.window = window
        self.loc = loc
        self.duration = duration
        self.active = None
        image_path = os.path.join('assets', 'images', 'ErrorImage', 'error.png')
        self._image = pygame.image.load(image_path).convert_alpha()

   def draw(self):
       self._startTime = pygame.time.get_ticks()
       self.active = True

   def freshPerFrame(self):
       if self.active:
          currentTime = pygame.time.get_ticks() 
          if currentTime - self._startTime <= self.duration:
              self.window.blit(self._image, self.loc)
          else:
              self.active = False
           
class InputData():
    def __init__(self, window, loc):
        self.window = window
        self.loc = loc
        self.background = AnimatedImage(self.window, loc, [resource_path("assets/images/inputdata/background.png")])
        self.enterBtn = AnimatedButton(self.window, (self.loc[0] + 500 - 170, self.loc[1] + 285), [resource_path("assets/images/inputdata/enterBtn_u.png")], [resource_path("assets/images/inputdata/enterBtn_d.png")])
        self.backBtn = AnimatedButton(self.window, (self.loc[0] + 100, self.loc[1] + 285), [resource_path("assets/images/inputdata/backBtn_u.png")], [resource_path("assets/images/inputdata/backBtn_d.png")])
        self.inputName = pygwidgets.InputText(self.window, (self.loc[0] + 100, self.loc[1] + 80), fontSize=40, width=300)
        self.inputServerIP = pygwidgets.InputText(self.window, (self.loc[0] + 100, self.loc[1] + 140), fontSize=40, width=300)

    def draw(self):
        self.background.draw()
        self.inputName.draw()
        self.inputServerIP.draw()
        self.enterBtn.draw()
        self.backBtn.draw()

    def handleEvent(self, event):
        self.inputName.handleEvent(event)
        self.inputServerIP.handleEvent(event)
        if self.backBtn.handleEvent(event):
            return (-1, "", "")
        if self.enterBtn.handleEvent(event):
            textName = self.inputName.getValue()
            textServerIP = self.inputServerIP.getValue()
            if textName != "" and textServerIP != "": return (1, textName, textServerIP)
        return (0, "", "")

