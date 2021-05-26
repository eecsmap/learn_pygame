import random
from random import randint
import pygame
from pygame.math import Vector2 as V2

pygame.init()

def scale(v, k):
    return type(v)(i // k for i in v)

def rand(v):
    return type(v)(random.randint(0, i) for i in v)

def rounds(v):
    return type(v)(*(round(i) for i in v))

WIDTH, HEIGHT = WIN_SIZE = scale(pygame.display.list_modes()[0], 4)
screen = pygame.display.set_mode(WIN_SIZE)

players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=scale(WIN_SIZE, 2))
    
    def update(self, sec):
        direct = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            direct[0] += 1
        if keys[pygame.K_LEFT]:
            direct[0] -= 1
        if keys[pygame.K_DOWN]:
            direct[1] += 1
        if keys[pygame.K_UP]:
            direct[1] -= 1
        if direct != [0, 0]:
            speed = 100 * V2(direct).normalize()
            self.rect.center += rounds(speed * sec)
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=rand(WIN_SIZE))
    
    def update(self):
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=scale(WIN_SIZE, 2))
        self.speed = randint(10, 50) * V2(0.5 - random.random(), 0.5 - random.random()).normalize()
        self.pos = pos
    
    def update(self, sec):
        self.pos += self.speed * sec
        self.rect.center = self.pos
        if self.rect.centerx < 0 or self.rect.centery > WIN_SIZE[0] \
            or self.rect.centery < 0 or self.rect.centery > WIN_SIZE[1]:
            self.kill()
        for e in pygame.sprite.spritecollide(self, enemies, True):
            pass
            #self.kill()
player = Player()
players.add(player)
FPS = 50
clock = pygame.time.Clock()
run = True
while run:
    run = not pygame.event.get(pygame.QUIT)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                bullets.add(Bullet(player.rect.center))
            if event.key == pygame.K_n:
                enemies.add(Enemy())

    sec = clock.tick(FPS) / 1000
    screen.fill('black')
    bullets.update(sec)
    players.update(sec)
    enemies.update()
    enemies.draw(screen)
    players.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()