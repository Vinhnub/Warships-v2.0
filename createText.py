import pygame

pygame.init()
# Đường dẫn tới file .ttf
font_path = "fonts/PressStart2P-Regular.ttf"  

# Load trực tiếp file
font = pygame.font.Font(font_path, 15)
text = font.render("Designed by Vinhnub", True, (0, 0, 0))
pygame.image.save(text, "text.png")