from utils import emit_event
import pygame

# from components import Transition
from interface import EventListener
from customevents import SCENEDONE, TRANSITION_DONE, TRANSITION_START
from scene import FadeTransition, MainMenuScene, NewGameScene, SettingsScene, TransitionScene
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
        self.on_event(TRANSITION_START, self.transition_start)
        self.on_event(TRANSITION_DONE, self.transition_done)
        self._set_active(start_scene)
        self.active.enter()

    def _set_active(self, scene_name):
        if scene_name in self.cached_scenes:
            self.active = self.cached_scenes[scene_name]
        else:
            self.active = self.cached_scenes[scene_name] = self.scenes[scene_name]()
            
    def transition_start(self, event):
        from_scene = self.active
        # to_scene = self.scenes[self.active.next]()
        to_scene = self.scenes[event.to_scene]()
        self.active = FadeTransition(from_scene, to_scene)
        
    def transition_done(self, event):
        #self.active.done = True
        if hasattr(event, 'scene'):            
            emit_event(SCENEDONE, scene=event.scene)

    def change(self, event):        
        # if hasattr(event, "scene"):
        #     if event.scene == self.active:
        self.previous = event.scene
        #self.active.exit()
        self.previous.exit()

        self._set_active(event.scene.name)
        self.active.enter()                

    def process_event(self, event) -> None:
        if event.type in self.listeners:
            self.handle_event(event)
        self.active.process_event(event)

    def update(self, dt):
        self.active.update(dt)


    def draw(self, screen):
        self.active.draw(self.screen)
        screen.blit(self.screen, self.screen_rect)
