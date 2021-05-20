import sys
import random
import pygame

pygame.init()

WIDTH, HEIGHT = SCREEN_SIZE = pygame.display.list_modes()[0]

screen = pygame.display.set_mode(SCREEN_SIZE)
FPS = 50
clock = pygame.time.Clock()

font = pygame.font.Font('JetBrainsMonoNL-Regular.ttf', 72)

target_value = random.randint(0, 15)

text_surf = font.render(f'{target_value:02x}', True, 'red')

score_surf = font.render('SCORE:', True, 'white')

class Bit(pygame.sprite.Sprite):
    def __init__(self, id, value=0):
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.is_focused = False
        self.image = font.render(f'{self.value}', True, 'green')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((WIDTH / 5 * (4-id), HEIGHT - 100))

    def set_focus(self, focused):
        self.is_focused = focused

    def update(self):
        self.image = font.render(f'{self.value}', True, 'green' if self.is_focused else 'blue')

all_sprites = pygame.sprite.Group()

bits = []
for i in range(4):
    bit = Bit(i)
    bits.append(bit)
    all_sprites.add(bit)

chosen = 3

score = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            chosen += 1
            chosen = chosen % 4
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            chosen -= 1
            chosen = chosen % 4
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            bits[chosen].value = bits[chosen].value ^ 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            value = 0
            for i in range(4):
                value |= bits[i].value << i
            if value == target_value:
                print('pass')
                score += 1
                target_value = random.randint(0, 15)
            else:
                print('fail')
                score -= 1
            for i in range(4):
                bits[i].value = 0
            chosen = 3

    for i, bit in enumerate(bits):
        bit.set_focus(i == chosen)

    score_surf = font.render(f'SCORE: {score:-5}', True, 'white')
    screen.fill('black')

    screen.blit(score_surf, (0, 0))
    text_surf = font.render(f'{target_value:02x}', True, 'red')
    screen.blit(text_surf, ((WIDTH - text_surf.get_width())/2, 0))

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
