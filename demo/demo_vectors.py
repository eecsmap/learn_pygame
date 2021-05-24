import pygame
from pygame.constants import FULLSCREEN
from pygame.math import Vector2
import random
import math

pygame.init()
WIDTH, HEIGHT = WIN_SIZE = [i // 2 for i in pygame.display.list_modes()[0]]
screen = pygame.display.set_mode(WIN_SIZE)

star = pygame.image.load('star.png').convert_alpha()

k = 10

all_mass = pygame.sprite.Group()

def in_rect(point, rect):
    return (rect.left < point.x and point.x < rect.right) and (rect.top < point.y and point.y < rect.bottom)

clock = pygame.time.Clock()
time_passed = clock.tick()

class M(pygame.sprite.Sprite):
    id = 0
    def __init__(self, pos=None, vel=None, mass=1):
        super().__init__()
        self.id = M.id
        M.id += 1
        self.mass = mass #random.randint(1, 1000)
        self.scale = self.mass
        self.image = pygame.transform.scale(star, (5, 5))
        #self.image.fill('white')
        self.rect = self.image.get_rect()
        self.position = pos if pos is not None else Vector2(random.randint(WIDTH/ 10, WIDTH/ 2), random.randint(0, HEIGHT/ 2))
        self.velocity = vel if vel is not None else Vector2(random.randint(0, 50), random.randint(0, 50))

    def __str__(self):
        return f'({self.id} {self.mass} {self.velocity})'

    def update(self):
        acceleration = Vector2()
        for other in all_mass:
            if other == self: continue
            direction = other.position - self.position
            distance_square = direction.magnitude_squared()

            if distance_square < 4:
                total_mass = self.mass + other.mass
                other.velocity = (self.mass * self.velocity + other.mass * other.velocity) / total_mass
                other.mass = total_mass
                self.mass = 0
                self.velocity = Vector2()
                self.kill()
                break

            if direction:
                direction.normalize_ip()
            acceleration += k * self.mass * other.mass / distance_square * direction / self.mass

        self.velocity += acceleration * time_passed
        self.position += self.velocity * time_passed
        #self.image = pygame.transform.scale(star, (self.mass, self.mass))
        self.rect.center = self.position

        if not in_rect(self.position, screen.get_rect()):
            self.kill()

run = True
#pygame.mouse.set_visible(False)

start_pos = Vector2()

GET_MASS, GET_VEL = 0, 1
state = GET_MASS
mass = 1
tick_sum = 0
i = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = Vector2(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = Vector2(event.pos)
            vel = end_pos - start_pos
            all_mass.add(M(pos=start_pos, vel=vel, mass = 100000 if i == 0 else 1))
            i += 1

    time_passed = clock.tick() / 1000
    screen.fill('black')
    if any(pygame.mouse.get_pressed()):
        pygame.draw.line(screen, 'white', start_pos, pygame.mouse.get_pos())
    all_mass.update()
    all_mass.draw(screen)
    pygame.display.flip()

pygame.quit()