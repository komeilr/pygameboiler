from interface import EventListener
from customevents import SCENEDONE
from scenes import SplashScene, MenuScene, SettingsScene


class SceneManager(EventListener):
    def __init__(self, controller, start_scene):
        super().__init__()
        self.controller = controller

        self.scenes = {
            "SPLASHSCENE": SplashScene,
            "MENUSCENE": MenuScene, 
            "SETTINGSSCENE": SettingsScene
        }

        self.cached_scenes = {}

        self.previous = None
        self.active = None
        
        self._set_active(start_scene)

        self.on_event(SCENEDONE, self.change)

    def _set_active(self, scene_name):
        if scene_name in self.cached_scenes:
            self.active = self.cached_scenes[scene_name]
        else:
            self.active = self.cached_scenes[scene_name] = self.scenes[scene_name]()
        
        self.active.enter()

    def change(self, event):
        if hasattr(event, 'scene'):
            if event.scene == self.active:
                self.previous = self.active
                self.active.exit()
                self._set_active(self.active.next)

    def process_event(self, event):
        if event.type in self.listeners:
            self.handle_event(event)
        self.active.process_event(event)

    def update(self, dt):
        self.active.update(dt)

    def draw(self, screen):
        self.active.draw(screen)
