import pygame
from constants import SCREEN_SIZE
from logger import l


l.info("Initializing pygame.mixer")  # debug
pygame.mixer.pre_init(44100, 16, 2, 4096)

l.info("Initialiing pygame")  # debug
pygame.init()

l.info(f"Initilaizing display {SCREEN_SIZE}")  # debug
# flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED
pygame.display.set_mode(SCREEN_SIZE)  # , flags=flags)


def teardown():
    pygame.quit()
