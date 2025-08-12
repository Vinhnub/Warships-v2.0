import pygame

pygame.init()
# Đường dẫn tới file .ttf
font_path = "fonts/Roboto-Black.ttf"  

# Load trực tiếp file
font = pygame.font.Font(font_path, 50)
text = font.render("YOU WIN", True, (0, 0, 0))
pygame.image.save(text, "textWIN.png")