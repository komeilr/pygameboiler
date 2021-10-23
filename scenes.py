import pygame
from interface import EventListener
from customevents import SCENEDONE
from inputhandler import Input
from utils import emit_event
from components import Button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Scene(EventListener):
    def __init__(self):
        super().__init__()
        self.done = False
        self.name = "Base Scene"
        self.next = ""    

    def process_event(self, event):
        pass        

    def update(self, dt):
        self.check_done()

    def draw(self, screen):
        pass

    def scene_done(self, next=None):
        self.done = True
        if next is not None:
            self.next = next

    def check_done(self):
        if self.done:
            emit_event(SCENEDONE, scene=self)

    def enter(self):
        pass

    def exit(self):
        self.done = False

    def switch_scene(self, next=None):        
        if next is not None:
            self.next = next
        self.done = True


class SplashScene(Scene):
    def __init__(self):
        super().__init__()        
        self.name = "SPLASHSCENE"
        self.next = "MENUSCENE"
        self.background = pygame.Color('black')  # change bg

        self.btn_new = Button('NEW', 50, 50, 100, 50)
        self.btn_new.set_position(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, centered=True)
        self.btn_new.bind('on_release', self.switch_scene, next='MENUSCENE')

        self.btn_settings = Button('SETTINGS', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 200, 50)
        self.btn_settings.set_position(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, centered=True)
        self.btn_settings.bind('on_release', self.switch_scene, next='SETTINGSSCENE')        

    def process_event(self, event):
        self.btn_new.process_event(event)
        self.btn_settings.process_event(event)
        if Input.is_action_just_pressed('ui_up'):
            self.scene_done()        

    def update(self, dt):        
        self.btn_new.update(dt)
        self.btn_settings.update(dt)
        self.check_done()

    def draw(self, screen):
        screen.fill(self.background)
        self.btn_new.draw(screen)
        self.btn_settings.draw(screen)
        # screen.blit(self.megaman_image, self.megaman_rect)


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "MENUSCENE"
        self.next = "SPLASHSCENE"
        self.background = pygame.Color('violet')

        self.btn_back = Button('BACK', 50, 50, 100, 50)
        self.btn_back.set_position(SCREEN_WIDTH * 0.87, SCREEN_HEIGHT - 50, centered=True)
        self.btn_back.bind('on_release', self.switch_scene, next='SPLASHSCENE')
        self.btn_back.config(
            pressed_color=pygame.Color('white'),
            hover_color=pygame.Color('red'),
            normal_color=pygame.Color('blue')
        )

    def process_event(self, event):
        self.btn_back.process_event(event)

    def update(self, dt):
        self.btn_back.update(dt)
        self.check_done()

    def draw(self, screen):
        screen.fill(self.background)
        self.btn_back.draw(screen)


class SettingsScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "SETTINGSSCENE"
        self.next = "SPLASHSCENE"
        self.background = pygame.Color('gray20')

        self.btn_back = Button('BACK', 50, 50, 100, 50)
        self.btn_back.set_position(SCREEN_WIDTH * 0.87, SCREEN_HEIGHT - 50, centered=True)
        self.btn_back.bind('on_release', self.switch_scene, next='SPLASHSCENE')

    def process_event(self, event):

        self.btn_back.process_event(event)
        # if Input.is_action_just_pressed('ui_down'):
        #     self.scene_done()

    def update(self, dt):        
        self.btn_back.update(dt)
        self.check_done()

    def draw(self, screen):
        screen.fill(self.background)
        self.btn_back.draw(screen)
        
