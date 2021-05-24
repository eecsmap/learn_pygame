import pygame
from pygame.constants import SRCALPHA

pygame.init()
WIN_SIZE = [i // 4 for i in pygame.display.list_modes()[0]]

screen = pygame.display.set_mode(WIN_SIZE)

s = pygame.Surface((50, 50)) # 24bit each pixel, r, g, b [0, 255]
s = pygame.Surface((50, 50), SRCALPHA) # 32bit each pixel, r, g, b, alpha

s.fill('red')
pygame.image.save(s, 'block.bmp')
