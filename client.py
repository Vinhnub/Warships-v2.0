import pygame
from pygame.locals import *
from constants import *
import sys
import random
from player import *
from network import *
from mySignal import *

oPlayer = Player(NetWork('192.168.1.28'))
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()


    window.fill(BLACK)

    pygame.display.update()
    
    clock.tick(FRAMES_PER_SECOND) 
    fps = int(clock.get_fps())
    pygame.display.set_caption(f"WAR SHIP V2.0 (FPS: {fps})")
