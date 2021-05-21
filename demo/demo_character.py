import pygame

pygame.mixer.pre_init(44100, 32, 2, 4096)
pygame.mixer.init()
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

snow_walk = pygame.mixer.Sound('SnowWalk.ogg')

class Player(pygame.sprite.Sprite):
    def __init__(self, controls):
        super(Player, self).__init__()
        self.raw_image = pygame.image.load('warrior_f.png').convert_alpha()
        self.raw_bubble = pygame.image.load('balloon_16.png').convert_alpha()
        self.width = 32
        self.height = 36
        self.index = 1 # still frame
        self.frame = 4
        self.images = {
            UP: [self.raw_image.subsurface((self.width * col, self.height * UP), (self.width, self.height)) for col in range(self.frame - 1)],
            RIGHT: [self.raw_image.subsurface((self.width * col, self.height * RIGHT), (self.width, self.height)) for col in range(self.frame - 1)],
            DOWN: [self.raw_image.subsurface((self.width * col, self.height * DOWN), (self.width, self.height)) for col in range(self.frame - 1)],
            LEFT: [self.raw_image.subsurface((self.width * col, self.height * LEFT), (self.width, self.height)) for col in range(self.frame - 1)],
        }
        for i in range(4):
            # add the missing middle frame
            self.images[i].append(self.images[i][1])
        self.direction = DOWN
        self.bubble_height = 16
        self.bubble_index = 0
        self.image = pygame.Surface((self.width, self.height + self.bubble_height))
        self.image.blit(self.raw_bubble.subsurface((16 * self.bubble_index, 0), (16, 16)), (self.width - 16, 0))
        self.image.blit(self.images[self.direction][self.index], (0, self.bubble_height))
        self.rect = self.image.get_rect()
        self.sum = 0
        self.vectors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.is_moving = False
        # two full steps (4 half steps) per sec in 4 frames walks about self.width
        self.step_width = self.width // self.frame
        self.controls = controls

    def update(self, millisecond):
        keys = pygame.key.get_pressed()
        new_direction = None
        if keys[self.controls[UP]]: new_direction = UP
        if keys[self.controls[DOWN]]: new_direction = DOWN
        if keys[self.controls[RIGHT]]: new_direction = RIGHT
        if keys[self.controls[LEFT]]: new_direction = LEFT
        self.is_moving = new_direction is not None
        if new_direction == None:
            self.index = 1
            self.is_moving = False
        else:
            self.is_moving = True
            if new_direction != self.direction:
                self.direction = new_direction
                self.index = 0

        self.sum += millisecond
        # every 4 frames is two steps
        if self.sum > 1000 / 4: # 4 frames per sec to make four half/small steps per sec
            self.sum = 0
            if self.is_moving:
                self.index += 1
                self.index = self.index % self.frame
                if self.index in [0, 2]:
                    snow_walk.play()
                self.rect.move_ip(* (self.step_width * i for i in self.vectors[self.direction]))
            else:
                self.index = 1
            #self.image.fill('black')
            self.image = pygame.Surface((self.width, self.height + self.bubble_height), 0, 32)
            self.bubble_index += 1
            self.bubble_index = self.bubble_index % 8
            self.image.blit(self.raw_bubble.subsurface((16 * self.bubble_index, 0), (16, 16)), (self.width - 16, 0))
            self.image.blit(self.images[self.direction][self.index], (0, self.bubble_height))
            self.image.set_colorkey('black')

player1 = Player((pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT))
all_players = pygame.sprite.Group()
all_players.add(player1)
player2 = Player((pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a))
all_players.add(player2)
clock = pygame.time.Clock()
run = True
direction = DOWN
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill('grey')
    all_players.update(clock.tick(50))
    all_players.draw(screen)
    pygame.display.flip()

pygame.quit()
