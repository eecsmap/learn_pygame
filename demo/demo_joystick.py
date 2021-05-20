from joysticks import JoystickManager
import pygame
import sys

from pygame.constants import JOYAXISMOTION

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))


joystick_manager = JoystickManager()

my_font = pygame.font.SysFont('JetBrainsMonoNL-Regular.ttf', 64)

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        joystick_manager.handle(event)

    screen.fill('black')
    x = y = 0
    if joystick_manager.joysticks:
        x = int(joystick_manager.joysticks[0].get_axis(0) * 250)
        y = int(joystick_manager.joysticks[0].get_axis(1) * 250)
    else:
        screen.blit(my_font.render('insert joystick ...', True, 'red'), (0, 0))

    pygame.draw.line(screen, 'red', (WIDTH / 2, HEIGHT / 2), ((WIDTH + x) / 2, (HEIGHT + y) / 2), 10)

    pygame.display.update()
    clock.tick(50)