import pygame
import sys

pygame.init()
WIN_SIZE = [i // 2 for i in pygame.display.list_modes()[0]]

screen = pygame.display.set_mode(WIN_SIZE)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in range(10):
        screen.set_at((10+i, 10), (150 + 10 * i, 0, 0))
    pygame.display.flip()

pygame.image.save(screen, 'hello.bmp')
pygame.quit()