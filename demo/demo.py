import pygame
pygame.init()

FULL_SCREEN_SIZE = pygame.display.list_modes()[0]
WIN_SIZE = [i // 4 for i in FULL_SCREEN_SIZE]

screen = pygame.display.set_mode(WIN_SIZE)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()

pygame.quit()
