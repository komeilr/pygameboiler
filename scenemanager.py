from interface import IEvent
from customevents import SCENEDONE
from scenes import SplashScene, MenuScene


class SceneManager(IEvent):
    def __init__(self, controller, start_scene):
        self.controller = controller
        self.scenes = {
            "SPLASHSCENE": SplashScene,
            "MENUSCENE": MenuScene
        }

        self.cached_scenes = {}

        self.previous = None
        self.active = None
        
        self._set_active(start_scene)

        self.listeners = {}
        self.on_event(SCENEDONE, self.change)

    def _set_active(self, scene_name):
        if scene_name in self.cached_scenes:
            self.active = self.cached_scenes[scene_name]
        else:
            self.active = self.cached_scenes[scene_name] = self.scenes[scene_name]()
        
        self.active.enter()

    def handle_event(self, event):
        for func, args in self.listeners[event.type]:
            func(event, *args)

    def on_event(self, event_type, cb, *args):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append((cb, args))

    def change(self, event):
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
