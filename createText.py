import pygame

pygame.init()
# Đường dẫn tới file .ttf
font_path = "fonts/PressStart2P-Regular.ttf"  

# Load trực tiếp file
font = pygame.font.Font(font_path, 50)
text = font.render("Exit", True, (255, 255, 255))
pygame.image.save(text, "text.png")