import pygame
from config import init_load
from constants import SCREEN_SIZE
from logger import l


l.info("Initializing pygame.mixer")  # debug
pygame.mixer.pre_init(44100, 16, 2, 4096)

l.info("Initialiing pygame")  # debug
pygame.init()

configsettings = init_load()


l.info(f"Initilaizing display {SCREEN_SIZE}")  # debug
l.info(f"Fullscreen: {configsettings.display['fullscreen']}")
flags = 0
vscyn = 0
if configsettings.display['fullscreen']:
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED
    vsync = 1
pygame.display.set_mode(SCREEN_SIZE, flags=flags, vsync=vsync)




def teardown():
    pygame.quit()
