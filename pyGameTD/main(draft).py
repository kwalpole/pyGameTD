# Keegan Walpole
# Tower Defense Game

# 1 - import
import pygame
print(pygame.font.get_fonts())
import os

# 2 - Class Building

# 3 - Class Initializing

# 4 - Game Logic
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# screen states
menu = True

# 5 - Running
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # main menu
    if menu == True:
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        screen.fill((153, 255, 187))
        if pygame.font:
            font = pygame.font.Font(None, 64)
            text = font.render("PyGameTD", True, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
            background.blit(text, textpos)
    else:
        bGimage = pygame.image.load("assets/Map.png")
        background_image = pygame.transform.scale(bGimage, screen.get_size())
        screen.blit(background_image, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
