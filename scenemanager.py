import pygame

# from components import Transition
from interface import EventListener
from customevents import SCENEDONE, TRANSITION_DONE
from scene import MainMenuScene, NewGameScene, SettingsScene
from constants import SCREEN_SIZE
from logger import l


class SceneManager(EventListener):
    def __init__(self, controller, start_scene):
        super().__init__()
        self.controller = controller
        self.screen = pygame.surface.Surface(SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()

        self.scenes = {
            "MAINMENUSCENE": MainMenuScene,
            "NEWGAMESCENE": NewGameScene,
            "SETTINGSSCENE": SettingsScene,
        }
        
        self.cached_scenes = {}

        self.previous = None
        self.active = None
        self.on_event(SCENEDONE, self.change)
        self._set_active(start_scene)
        self.active.enter()

    def _set_active(self, scene_name):
        if scene_name in self.cached_scenes:
            self.active = self.cached_scenes[scene_name]
        else:
            self.active = self.cached_scenes[scene_name] = self.scenes[scene_name]()

    def change(self, event):
        if hasattr(event, "scene"):
            if event.scene == self.active:
                self.previous = self.active
                self.active.exit()

                self._set_active(self.active.next)

    def process_event(self, event) -> None:
        if event.type in self.listeners:
            self.handle_event(event)
        self.active.process_event(event)

    def update(self, dt):
        self.active.update(dt)


    def draw(self, screen):
        self.active.draw(self.screen)
        screen.blit(self.screen, self.screen_rect)
