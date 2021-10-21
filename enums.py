from enum import Enum

class RenderLayer(Enum):
    BG1 = 0
    BG2 = 1
    WORLD = 2
    ITEMS = 3
    PROJECTILES = 4
    ENEMIES = 5
    PLAYER = 6
    HUD = 7
    TRANSITION = 8