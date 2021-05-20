import pygame
from pygame.constants import SRCALPHA

pygame.init()
WIN_SIZE = [i // 4 for i in pygame.display.list_modes()[0]]

screen = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()
print(clock.tick(100))

print(clock.tick(1))

print(clock.tick(1))