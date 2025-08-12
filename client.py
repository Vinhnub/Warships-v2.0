import pygame
from pygame.locals import *
from constants import *
import sys
import random
import time
from player import *
from network import *
from mySignal import *
from widget import *
from gameandscreen import *
from main import *

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
main = Main(window)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()
        main.handleEvent(event)
    window.fill(BLACK)

    main.draw()

    pygame.display.update()
    
    
    clock.tick(FRAMES_PER_SECOND) 
    fps = int(clock.get_fps())
    pygame.display.set_caption(f"WAR SHIP V2.0 (FPS: {fps})")

    