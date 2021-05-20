import pygame
pygame.init()

FULL_SCREEN_SIZE = pygame.display.list_modes()[0]
WIN_SIZE = [i // 4 for i in FULL_SCREEN_SIZE]

screen = pygame.display.set_mode(WIN_SIZE)
#screen = pygame.display.set_mode(FULL_SCREEN_SIZE, pygame.FULLSCREEN | pygame.DOUBLEBUF)

fontnames = pygame.font.get_fonts()
font_cursor = 0
nfonts = len(fontnames)
fontname = fontnames[0]

def centered(parent, target):
    x = (parent.get_width() - target.get_width()) / 2
    y = (parent.get_height() - target.get_height()) / 2
    return x, y

block = pygame.Surface((100, 50))
block.fill('yellow')
block.get_rect(center=[i // 2 for i in WIN_SIZE])
font_height = 48
font = pygame.font.SysFont(None, font_height)

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.raw_image = pygame.image.load('warrior_f.png').convert_alpha()
        self.width = 32
        self.height = 36
        self.index = 1 # still frame
        self.frame = 3
        self.images = {
            UP: [self.raw_image.subsurface((self.width * col, self.height * UP), (self.width, self.height)) for col in range(self.frame)],
            RIGHT: [self.raw_image.subsurface((self.width * col, self.height * RIGHT), (self.width, self.height)) for col in range(self.frame)],
            DOWN: [self.raw_image.subsurface((self.width * col, self.height * DOWN), (self.width, self.height)) for col in range(self.frame)],
            LEFT: [self.raw_image.subsurface((self.width * col, self.height * LEFT), (self.width, self.height)) for col in range(self.frame)],
        }
        self.direction = DOWN
        self.image = self.images[self.direction][self.index]
        self.rect = self.image.get_rect()
        self.sum = 0
        self.vectors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.speed = 400
        self.is_moving = False

    def update(self, millisecond):
        keys = pygame.key.get_pressed()
        new_direction = None
        if keys[pygame.K_UP]: new_direction = UP
        if keys[pygame.K_DOWN]: new_direction = DOWN
        if keys[pygame.K_RIGHT]: new_direction = RIGHT
        if keys[pygame.K_LEFT]: new_direction = LEFT
        self.is_moving = new_direction is not None
        if new_direction == None:
            self.index = 1
        elif new_direction != self.direction:
            self.direction = new_direction
            self.index = 0

        self.sum += millisecond
        if self.sum > 1000 / 6: # 6 frames per sec
            self.sum = 0
            if self.is_moving:
                self.index += 1
                self.index = self.index % self.frame
                self.rect.move_ip(* (self.speed * millisecond / 1000 * i for i in self.vectors[self.direction]))
            else:
                self.index = 1
            self.image = self.images[self.direction][self.index]

player = Player()
all_players = pygame.sprite.Group()
all_players.add(player)
clock = pygame.time.Clock()
run = True
direction = DOWN
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill('black')
    all_players.update(clock.tick(50))
    all_players.draw(screen)
    pygame.display.flip()

pygame.quit()
