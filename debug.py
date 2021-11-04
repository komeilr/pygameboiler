import pygame
from content import Content


try:
    font = Content.Font.get_font('Inconsolata_20')
except ValueError as e:
    print(e)
    print("Loading default sysfont 'Arial' ")
    font = pygame.font.SysFont('Arial', 20)


def debug_info(info, y=10, x=10):

    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, pygame.Color('white'))
    rect = debug_surf.get_rect()
    rect.topleft = (x, y)
    pygame.draw.rect(display_surf, pygame.Color('black'), rect)

    display_surf.blit(debug_surf, rect)
