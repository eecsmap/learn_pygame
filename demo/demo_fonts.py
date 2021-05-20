import pygame
pygame.init()

FULL_SCREEN_SIZE = pygame.display.list_modes()[0]
WIN_SIZE = [i // 4 for i in FULL_SCREEN_SIZE]

screen = pygame.display.set_mode(WIN_SIZE)

fontnames = pygame.font.get_fonts()
font_cursor = 0
nfonts = len(fontnames)
fontname = fontnames[0]
'''
chinese supported:
    microsoftyaheimicrosoftyaheiui
    microsoftyaheimicrosoftyaheiuibold
    microsoftyaheimicrosoftyaheiuilight
    msgothicmsuigothicmspgothic
    simsunnsimsun
    yugothicyugothicuisemiboldyugothicuibold
    yugothicyugothicuilight
    yugothicmediumyugothicuiregular
    yugothicregularyugothicuisemilight
    dengxian
    fangsong
    kaiti
    simhei
'''

def centered(parent, target):
    x = (parent.get_width() - target.get_width()) / 2
    y = (parent.get_height() - target.get_height()) / 2
    return x, y

block = pygame.Surface((100, 50))
block.fill('yellow')
block.get_rect(center=[i // 2 for i in WIN_SIZE])
font_height = 48

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            font_height += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            font_height -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            font_cursor -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            font_cursor += 1
        if event.type == pygame.KEYDOWN:
            fontname = fontnames[font_cursor % nfonts]
            font_height = min((max(8, font_height), 100))
            print(fontname)

    font = pygame.font.SysFont(fontname, font_height)
    text = font.render(f'{fontname} of size {font_height}', True, 'white')
    screen.fill('black')
    screen.blit(text, centered(screen, text))  
    pygame.display.flip()

pygame.quit()
