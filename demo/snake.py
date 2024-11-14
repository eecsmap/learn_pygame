import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLUE, PINK, (0, 0, 255), (255, 255, 0)]  # Colors for up to 4 players

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Snake Game")

# Game variables
clock = pygame.time.Clock()
snake_speed = 10

# Snake and Food Classes
class Snake:
    def __init__(self, color, start_pos):
        self.base_color = color
        self.flash_color = WHITE  # Snake flashes white when 'B' button is pressed
        self.color = color
        self.body = [start_pos]
        self.direction = pygame.Vector2(1, 0)  # Initially moving to the right
        self.alive = True
        self.flash_timer = 0  # Timer to control flashing duration

    def move(self):
        if self.alive:
            new_head = self.body[0] + self.direction * CELL_SIZE
            self.body = [new_head] + self.body[:-1]

    def grow(self):
        if self.alive:
            new_head = self.body[0] + self.direction * CELL_SIZE
            self.body = [new_head] + self.body

    def check_collision(self, width, height):
        # Wall collision
        head = self.body[0]
        if head.x < 0 or head.x >= width or head.y < 0 or head.y >= height:
            self.alive = False

        # Self-collision
        if head in self.body[1:]:
            self.alive = False

    def flash(self):
        self.flash_timer = 10  # Flash for a short period

    def draw(self):
        # Update color based on flash timer
        if self.flash_timer > 0:
            self.color = self.flash_color
            self.flash_timer -= 1
        else:
            self.color = self.base_color

        # Draw snake
        for part in self.body:
            pygame.draw.rect(screen, self.color, pygame.Rect(part.x, part.y, CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                                       random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def respawn(self):
        self.position = pygame.Vector2(random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                                       random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def draw(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position.x, self.position.y, CELL_SIZE, CELL_SIZE))


# Joystick setup
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

# Initialize snakes and food
def initialize_game():
    global snakes, food
    snakes = [Snake(COLORS[i], pygame.Vector2(CELL_SIZE * (i + 1), CELL_SIZE)) for i in range(min(len(joysticks), 4))]
    food = Food()

initialize_game()

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not all(snake.alive for snake in snakes):
        # Restart game if button 0 is pressed
        if any(joystick.get_button(0) for joystick in joysticks):
            print("restarting game")
            initialize_game()

    # Joystick movement and flash handling
    for i, joystick in enumerate(joysticks):
        if i < len(snakes) and snakes[i].alive:
            # Flash snake if 'B' button (usually button index 1) is pressed
            if joystick.get_button(1):
                snakes[i].flash()

            # Control movement with joystick axes
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)
            # Move left/right
            if abs(x_axis) > abs(y_axis):
                if x_axis < -0.2 and snakes[i].direction != pygame.Vector2(1, 0):
                    snakes[i].direction = pygame.Vector2(-1, 0)
                elif x_axis > 0.2 and snakes[i].direction != pygame.Vector2(-1, 0):
                    snakes[i].direction = pygame.Vector2(1, 0)
            # Move up/down
            elif abs(y_axis) > abs(x_axis):
                if y_axis < -0.2 and snakes[i].direction != pygame.Vector2(0, 1):
                    snakes[i].direction = pygame.Vector2(0, -1)
                elif y_axis > 0.2 and snakes[i].direction != pygame.Vector2(0, -1):
                    snakes[i].direction = pygame.Vector2(0, 1)

    # Move snakes and check for collisions
    for snake in snakes:
        snake.move()
        snake.check_collision(SCREEN_WIDTH, SCREEN_HEIGHT)
        # Check if snake eats the food
        if snake.alive and snake.body[0] == food.position:
            snake.grow()
            food.respawn()

    # Draw food and snakes
    food.draw()
    for snake in snakes:
        snake.draw()

    pygame.display.flip()
    clock.tick(snake_speed)

# Quit Pygame
pygame.quit()
