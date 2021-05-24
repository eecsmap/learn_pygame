import pygame
from pygame.math import Vector2
pygame.init()


def ints(v):
    return [*(round(i) for i in v)]

clock = pygame.time.Clock()
screen = pygame.display.set_mode(ints(Vector2(pygame.display.list_modes()[0]) / 2))

run = True
while run:
    quit = pygame.event.get(pygame.QUIT)
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEWHEEL:
            print(event)