import pygame
pygame.init()
window = pygame.display.set_mode((400, 500))
color = 'black'
height = 50
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        if (event.type == pygame.MOUSEBUTTONDOWN):
            color = 'red'; height = 30
        if (event.type == pygame.MOUSEBUTTONUP):
            color = 'blue'; height = 70

    window.fill('lightgrey')
    pygame.draw.line(window, color, (200, 400), (200, 300 - height), 50)
    pygame.display.flip()