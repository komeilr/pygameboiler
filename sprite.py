import pygame
from components import Position


class BaseSprite(pygame.sprite.DirtySprite):
    def __init__(self, group, layer=0):
        super().__init__(group)
        self._layer = layer
        self.position = Position(0, 0)
