import pygame
from interface import IEvent


class Level(IEvent):
    def __init__(self):
        self.render_group = pygame.sprite.LayeredDirty()

    def process_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, evt):
        pass

    def on_event(self, evt_type, cb, *args):
        pass
