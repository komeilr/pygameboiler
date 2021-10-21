import pygame
import init


from interface import IEvent
from scenemanager import SceneManager
from inputhandler import Input
from constants import FPS_RATE
from debug import debug_info
from customevents import DEBUG_TOGGLED
from utils import emit_event

from content import Content


class GameEngine(IEvent):

    def __init__(self, console_debug=False, debug=False):
        self.screen = pygame.display.get_surface()

        self.console_debug = console_debug
        self.debug = debug

        self.running = True
        self.timer = pygame.time.Clock()
        self.max_fps = FPS_RATE

        self.title = "My Game"

        self.listeners = {}

        self.on_event(pygame.QUIT, self.shutdown)
        self.on_event(pygame.KEYDOWN, self.key_pressed)
        self.on_event(pygame.KEYUP, self.key_released)
        self.on_event(DEBUG_TOGGLED, self.debug_toggled)

        self.scene_manager = SceneManager(self, "SPLASHSCENE")

        self.background_image = Content.Image.load('bg')
        self.bg_rect = self.background_image.get_rect()

    def run(self):

        self.setup()

        dt = 0

        while self.running:
            # process game events.
            for event in pygame.event.get():
                if self.console_debug:
                    print(event)

                if event.type in [pygame.KEYDOWN]:
                    Input.update_actions(event)

                if event.type in [pygame.KEYUP]:
                    Input.just_pressed = False

                if event.type in self.listeners:
                    self.handle_event(event)

                self.scene_manager.process_event(event)
                Input.reset_action_map()
            # l.info(self.listeners)  # debugs
            # update all the objects.
            self.update(dt)

            # draw stuff to the screen.
            self.draw()

            dt = self.timer.tick(self.max_fps) / 1000.0

        init.teardown()

    def process_event(self, event):
        pass

    def update(self, dt):
        self.scene_manager.update(dt)
        pass

    def draw(self):
        self.scene_manager.draw(self.screen)
        # self.screen.blit(self.background_image, self.bg_rect)  # debug for testing Image class
        if self.debug:
            debug_info(f"Scene: {self.scene_manager.active.name}")
            debug_info(f"FPS: {int(self.timer.get_fps())}", 30)
            # debug_info(f"dt: {pygame.time.get_ticks()}", 50)
        pygame.display.update()

    def update_title(self, title):
        if title == "":
            title = self.title
        else:
            title = "%s - %s" % (self.title, title)
        pygame.display.set_caption(title)

    def setup(self):
        self.update_title("")

    def shutdown(self, event):
        self.running = False

    @staticmethod
    def quit_pressed(event):
        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            emit_event(pygame.QUIT)

    def key_released(self, event):
        pass

    @staticmethod
    def key_pressed(event):
        if event.key == pygame.K_ESCAPE:
            emit_event(pygame.QUIT)

        if event.key == pygame.K_F3:
            emit_event(DEBUG_TOGGLED)

    def debug_toggled(self, event):
        self.debug = not self.debug

    def handle_event(self, evt):
        for func, args in self.listeners[evt.type]:
            func(evt, *args)

    def on_event(self, evt_type, cb, *args):
        if evt_type not in self.listeners:
            self.listeners[evt_type] = []
        self.listeners[evt_type].append((cb, args))
