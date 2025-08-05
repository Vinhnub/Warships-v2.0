import pygame

pygame.init()
# Đường dẫn tới file .ttf
font_path = "fonts/Roboto-Black.ttf"  

# Load trực tiếp file
font = pygame.font.Font(font_path, 30)
text = font.render("back", True, (0, 0, 0))
pygame.image.save(text, "text.png")