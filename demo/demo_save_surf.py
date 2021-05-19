import pygame

pygame.init()
WIN_SIZE = [i // 4 for i in pygame.display.list_modes()[0]]

screen = pygame.display.set_mode(WIN_SIZE)

s = pygame.Surface((50, 50))
s.fill('red')
pygame.image.save(s, 'block.bmp')
