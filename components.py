import pygame

from pygame.math import Vector2

from interface import IEvent
from content import Content
from utils import emit_event
from enums import RenderLayer
from customevents import ANIMATION_CHANGED, ON_PRESSED, ON_ENTER, ON_LEAVE


class Position(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)


class SpriteSheet:
    def __init__(self, image_name: str, h_frames, v_frames):
        try:
            self.image = Content.Image.load(image_name)
        except ValueError as e:
            print(e)

        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

        self.h_frames = h_frames
        self.v_frames = v_frames

        self.frame_width = self.width // h_frames
        self.frame_height = self.height // v_frames
        self.frame_coords = self._generate_frame_coords()

    def _generate_frame_coords(self):
        frame_dict = {}
        frame_num = 0

        for y in range(self.v_frames):
            for x in range(self.h_frames):
                frame_dict[frame_num] = (x * self.frame_width, y * self.frame_height, self.frame_width, self.frame_height)
                frame_num += 1
        return frame_dict

    def image_at_frame(self, frame, colorkey=None) -> pygame.surface.Surface:
        rect = pygame.Rect(self.frame_coords[frame])
        image = pygame.surface.Surface(rect.size).convert()
        image.blit(self.image, (0, 0),  rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def load_frames(self, start_frame, end_frame, colorkey=None) -> dict:
        frames = {}
        for i in range(end_frame - start_frame + 1):
            frames[i] = self.image_at_frame(start_frame + i, colorkey)
        return frames


class Animation:
    def __init__(self, name, spritesheet, frame_start, frame_end):
        self.name = name 
        self.frames = spritesheet.load_frames(frame_start, frame_end)

    def __len__(self):
        return len(self.frames)

    def get_frame(self, frame):
        return self.frames[frame]


class AnimationPlayer(IEvent):
    def __init__(self, entity):
        super().__init__()
        self.animations = {}
        self.current_animation = None
        self.frame = 0
        self.playback_speed = 8
        self.anim_time = 0

        self.on_event(ANIMATION_CHANGED, self.animation_changed)

    def animation_changed(self, event):
        pass        

    def update(self, dt):
        self.anim_time += dt

    def add_animation(self, animation_name, animation: Animation):
        self.animations[animation_name] = animation

    def set_animation(self, animation_name):
        if animation_name not in self.animations:
            raise AttributeError(f"{animation_name} not found in animations")
        self.current_animation = self.animations[animation_name]
        emit_event(ANIMATION_CHANGED)

    def play(self):
        pass

    def reset(self):
        pass

    def handle_event(self, evt):
        pass

    def on_event(self, evt_type, cb, *args):
        pass

    def draw(self, screen):
        pass

    def process_event(self, event):
        pass


class ButtonBase(IEvent):

    def __init__(self, x, y, w=0, h=0):
        self.position = Position(x, y)
        self.size = Position(w, h)
        self.rect = pygame.Rect(self.position.xy, self.size.xy)

        self.on_event(ON_ENTER, self._on_enter)
        self.on_event(ON_LEAVE, self._on_leave)
        self.on_event(ON_PRESSED, self._on_pressed)

    def _on_enter(self, event):
        pass

    def _on_leave(self, event):
        pass

    def _on_pressed(self, event):
        pass

    def handle_event(self, evt):
        pass

    def on_event(self, evt_type, cb, *args):
        pass


class Button(ButtonBase, pygame.sprite.DirtySprite):
    def __init__(self, image_name, x, y, group):        
        ButtonBase.__init__(self, x, y)
        pygame.sprite.DirtySprite.__init__(self, group)
        self._layer = RenderLayer.HUD

        self.image = Content.Image.load(image_name)
        self.rect = pygame.Rect(self.position.xy, self.image.get_size())

    def _on_enter(self, event):
        self.dirty = 1

    def _on_leave(self, event):
        self.dirty = 1

    def _on_pressed(self, event):
        self.dirty = 1

    def process_event(self, event):
        pass

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            emit_event(ON_ENTER)

    def draw(self, screen):
        pass

    def update_image(self, image_name):
        self.image = Content.Image.load(image_name)
