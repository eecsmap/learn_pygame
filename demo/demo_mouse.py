import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))

mouse_raw = pygame.image.load('star.png').convert_alpha()
mouse_surface = pygame.transform.scale(mouse_raw, (20, 20))

run = True
pygame.mouse.set_visible(False)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    x, y = pygame.mouse.get_pos()
    screen.fill('black')
    screen.blit(mouse_surface, (x - mouse_surface.get_width() / 2, y - mouse_surface.get_height() / 2))
    pygame.display.flip()

pygame.quit()