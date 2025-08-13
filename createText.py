import pygame

pygame.init()
# Đường dẫn tới file .ttf
font_path = "fonts/PressStart2P-Regular.ttf"  

# Load trực tiếp file
font = pygame.font.Font(font_path, 50)
text = font.render("Enter", True, (0, 0, 0))
pygame.image.save(text, "text.png")