import pygame
from pygame.locals import *
import sys
import random

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


while True:
    # handle event from keyboard, button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()
    
    window.fill(BLACK)
    

    pygame.display.update()
    
    
    clock.tick(FRAMES_PER_SECOND) 
    fps = int(clock.get_fps())
    pygame.display.set_caption(f"WAR SHIP V2.0 (FPS: {fps})")
