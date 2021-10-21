import pygame
from interface import IEvent
from customevents import SCENEDONE
from inputhandler import Input
from utils import emit_event
from components import SpriteSheet
from level import Level


class Scene(IEvent):
    def __init__(self):
        self.done = False
        self.name = "Base Scene"
        self.next = ""

        self.listeners = {}        

    def process_event(self, event):
        if event.type in self.listeners:
            self.handle_event(event)        

    def handle_event(self, evt):
        super().handle_event(evt)

    def on_event(self, evt_type, cb, *args):
        super().on_event(evt_type, cb, *args)

    def update(self, dt):
        self.check_done()

    def draw(self, screen):
        pass

    def scene_done(self):
        self.done = True

    def check_done(self):
        if self.done:
            emit_event(SCENEDONE)

    def enter(self):
        pass

    def exit(self):
        self.done = False


class SplashScene(Scene):
    def __init__(self):
        super().__init__()        
        self.name = "SPLASHSCENE"
        self.next = "MENUSCENE"
        self.background = pygame.Color('orange') # change bg

        self.frame = 0

        self.level = Level()

        self.megaman_ss = SpriteSheet('megaman_spritesheet', 5, 2)
        self.megaman_image = self.megaman_ss.image_at_frame(self.frame)
        self.megaman_rect = self.megaman_image.get_rect()

        self.mm_strip = self.megaman_ss.load_frames(0, 4)

    def process_event(self, event):
        super().process_event(event)

        if Input.is_action_just_pressed('ui_up'):
            self.scene_done()
        self.handle_event(event)

    def update(self, dt):
        self.check_done()

    def draw(self, screen):
        # screen.fill(self.background)
        screen.blit(self.megaman_image, self.megaman_rect)


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "MENUSCENE"
        self.next = "SPLASHSCENE"
        self.background = pygame.Color('violet')

    def process_event(self, event):
        super().process_event(event)
        if Input.is_action_just_pressed('ui_down'):
            self.scene_done()
        self.handle_event(event)

    def update(self, dt):
        self.check_done()

    def draw(self, screen):
        screen.fill(self.background)
