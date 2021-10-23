import pygame
from interface import EventListener
from customevents import SCENEDONE, ON_RELEASE
from inputhandler import Input
from utils import emit_event
from components import Button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from groups import layered_group
from enums import RenderLayer
from logger import l


class Scene(EventListener):
    def __init__(self):
        super().__init__()
        self.done = False
        self.name = "Base Scene"
        self.next = ""
        self.screen = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

    def process_event(self, event):
        pass        

    def update(self, dt):
        self.check_done()

    def draw(self, screen):
        pass

    def scene_done(self, next_scene=None):
        self.done = True
        if next_scene is not None:
            self.next = next_scene

    def check_done(self):
        if self.done:
            emit_event(SCENEDONE, scene=self)

    def enter(self):
        pass

    def exit(self):
        self.done = False

    def switch_scene(self, next_scene=None):
        if next_scene is not None:
            self.next = next_scene
        self.done = True


# ---------SPLASH SCENE-----------#
class SplashScene(Scene):
    def __init__(self):
        super().__init__()        
        self.name = "SPLASHSCENE"
        self.next = "MENUSCENE"
        self.background = pygame.Color(0, 0, 0, 0)  # change bg

        self.buttons = []
        self.layered_group = layered_group.copy()

        self.btn_new = Button('NEW', 50, 50, 100, 50, self.layered_group)
        self.btn_new.set_position(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, centered=True)
        self.btn_new.bind('on_release', self.switch_scene, next_scene='MENUSCENE')
        self.btn_new.config(
            pressed_color=pygame.Color('lightblue'),
            hover_color=pygame.Color('violet'),
            normal_color=pygame.Color('lightblue')
        )
        self.buttons.append(self.btn_new)

        self.btn_settings = Button('SETTINGS', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 200, 50, self.layered_group)
        self.btn_settings.set_position(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, centered=True)
        self.btn_settings.bind('on_release', self.switch_scene, next_scene='SETTINGSSCENE')
        self.btn_settings.config(
            pressed_color=pygame.Color('lightblue'),
            hover_color=pygame.Color('violet'),
            normal_color=pygame.Color('lightblue')
        )
        self.buttons.append(self.btn_settings)

        self.selected_index = 0
        self.selected = self.buttons[self.selected_index]

        l.info(f"splash: {self.layered_group.sprites()}")

    def process_event(self, event):

        if Input.is_action_just_pressed('ui_up'):
            self.selected_index -= 1
        if Input.is_action_just_pressed('ui_down'):
            self.selected_index += 1

        self.set_selected()

        if Input.is_action_just_pressed('ui_accept'):
            emit_event(ON_RELEASE, body=self.selected)

        self.btn_new.process_event(event)
        self.btn_settings.process_event(event)

    def update(self, dt):
        self.update_mouse_select()
        self.update_selected()
        self.btn_new.update(dt)
        self.btn_settings.update(dt)
        self.check_done()

    def update_mouse_select(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.selected_index = self.buttons.index(button)

    def set_selected(self):
        if self.selected_index > len(self.buttons) - 1:
            self.selected_index = 0

        elif self.selected_index < 0:
            self.selected_index = len(self.buttons) - 1

        self.selected = self.buttons[self.selected_index]

    def update_selected(self):
        for button in self.buttons:
            if button == self.selected:
                button.set_bold(0)
                button.border_width = 4
                button.color = pygame.Color('violet')
            else:
                button.set_bold(0)
                button.border_width = 1
                button.color = pygame.Color('lightblue')

    def draw(self, screen):
        self.screen.fill(self.background)
        self.btn_new.draw(self.screen)
        self.btn_settings.draw(self.screen)
        screen.blit(self.screen, self.screen_rect)
        # screen.blit(self.megaman_image, self.megaman_rect)


# ----------MENU SCENE------------#
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "MENUSCENE"
        self.next = "SPLASHSCENE"
        self.background = pygame.Color(0, 0, 0, 0)
        self.layered_group = layered_group.copy()

        self.btn_back = Button('BACK', 50, 50, 100, 50, self.layered_group)
        self.btn_back.set_position(SCREEN_WIDTH * 0.87, SCREEN_HEIGHT - 50, centered=True)
        self.btn_back.bind('on_release', self.switch_scene, next_scene='SPLASHSCENE')
        self.btn_back.config(
            pressed_color=pygame.Color('lightblue'),
            hover_color=pygame.Color('violet'),
            normal_color=pygame.Color('lightblue')
        )

        l.info(f"menu: {self.layered_group.sprites()}")

    def process_event(self, event):
        self.btn_back.process_event(event)

    def update(self, dt):
        self.btn_back.update(dt)
        self.check_done()

    def draw(self, screen):
        self.screen.fill(self.background)
        self.btn_back.draw(self.screen)
        screen.blit(self.screen, self.screen_rect)


# --------SETTINGS SCENE----------#
class SettingsScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "SETTINGSSCENE"
        self.next = "SPLASHSCENE"
        self.background = pygame.Color(0, 0, 0, 0)
        self.layered_group = layered_group.copy()

        self.btn_back = Button('BACK', 50, 50, 100, 50, self.layered_group)
        self.btn_back.set_position(SCREEN_WIDTH * 0.87, SCREEN_HEIGHT - 50, centered=True)
        self.btn_back.bind('on_release', self.switch_scene, next_scene='SPLASHSCENE')
        self.btn_back.config(
            pressed_color=pygame.Color('lightblue'),
            hover_color=pygame.Color('violet'),
            normal_color=pygame.Color('lightblue')
        )

        l.info(f"settings: {self.layered_group.sprites()}")

    def process_event(self, event):
        self.btn_back.process_event(event)
        # if Input.is_action_just_pressed('ui_down'):
        #     self.scene_done()

    def update(self, dt):        
        # self.btn_back.update(dt)
        self.layered_group.update(dt)
        self.check_done()

    def draw(self, screen):
        self.screen.fill(self.background)
        # self.layered_group.draw(screen)
        self.btn_back.draw(self.screen)
        screen.blit(self.screen, self.screen_rect)
        
