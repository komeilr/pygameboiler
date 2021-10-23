import pygame
from pygame.constants import MOUSEBUTTONUP

from pygame.math import Vector2

from inputhandler import Input
from interface import EventListener
from content import Content
from utils import emit_event
from enums import RenderLayer
from customevents import ANIMATION_CHANGED, ON_PRESSED, ON_ENTER, ON_LEAVE, ON_RELEASE
from logger import l


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
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def load_frames(self, start_frame, end_frame, colorkey=None) -> dict:
        frames = {}
        for i in range(end_frame - start_frame + 1):
            frames[i] = self.image_at_frame(start_frame + i, colorkey=colorkey)
        return frames


class Animation:
    def __init__(self, name, spritesheet, frame_start, frame_end):
        self.name = name 
        self.frames = spritesheet.load_frames(frame_start, frame_end)

    def __len__(self):
        return len(self.frames)

    def get_frame(self, frame):
        return self.frames[frame]


class AnimationPlayer(EventListener):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.animations = {}
        self.frame = 0
        self.playback_speed = 8
        self.anim_time = 0
        self.current_animation = None

        self.on_event(ANIMATION_CHANGED, self.animation_changed)

    def animation_changed(self, event):
        self.anim_time = 0     

    def update(self, dt):        
        time_per_frame = 1/self.playback_speed
        
        self.anim_time += dt
        if self.anim_time > time_per_frame * self.playback_speed:
            self.anim_time -= (time_per_frame * self.playback_speed)

        self.frame = self.anim_time // time_per_frame

    def set_animation(self, animation_name):
        if animation_name not in self.animations:
            raise AttributeError(f"{animation_name} not found in animations")
        self.current_animation = self.animations[animation_name]
        emit_event(ANIMATION_CHANGED)

    def add_animation(self, animation_name, animation: Animation):
        self.animations[animation_name] = animation

    def play(self):
        self.update_entity_image()

    def update_entity_image(self):
        self.entity.image = self.current_animation.get_frame(self.frame)
        self.entity.rect = self.entity.image.get_rect()

    def reset(self):
        pass


class ButtonBase(EventListener):
    def __init__(self, x, y, w=0, h=0):
        super().__init__()
        self.position = Position(x, y)
        self.size = Position(w, h)
        self.rect = pygame.Rect(self.position.xy, self.size.xy)

        self.disabled = False
        self.state_commands = {}

        self.normal_color = pygame.Color('white')
        self.hover_color = pygame.Color('white')
        self.pressed_color = pygame.Color('white')
        self.released_color = pygame.Color('white')

        self.on_event(ON_ENTER, self._on_enter)
        self.on_event(ON_LEAVE, self._on_leave)
        self.on_event(ON_PRESSED, self._on_pressed)
        self.on_event(ON_RELEASE, self._on_release)
        self.on_event(MOUSEBUTTONUP, self._on_release)

    def config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _on_enter(self, event):
        pass

    def _on_leave(self, event):
        pass

    def _on_pressed(self, event, command=None):
        pass

    def _on_release(self, event):
        pass

    def process_event(self, event):
        pass

    def set_disabled(self, val):
        if not isinstance(val, bool):
            raise ValueError("value must be boolean")
        self.disabled = val

    def set_position(self, x, y, centered=False):
        if centered:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def bind(self, button_state, command, *args, **kwargs):
        if button_state not in self.state_commands:
            self.state_commands[button_state] = [command, args, kwargs]
        

class Button(ButtonBase, pygame.sprite.DirtySprite):
    def __init__(self, image_name, x, y, w, h, group):
        self._layer = RenderLayer.HUD.value
        ButtonBase.__init__(self, x, y, w, h)
        pygame.sprite.DirtySprite.__init__(self, group)


        try:
            self.image = Content.Image.load(image_name)        
            self.rect = pygame.Rect(self.position.xy, self.image.get_size())
        except ValueError as e:
            print(f"{e} - Using text - {image_name}")
            self.rect = pygame.Rect(self.position.xy, (w, h))
            self.text = image_name

        self.color = pygame.Color('gray')
        self.border_width = 1
        self.bold = 0

        self.mouse_entered = False

    def _on_enter(self, event, **kwargs):
        if hasattr(event, 'body'):
            if event.body == self:
                self.dirty = 1
                self.mouse_entered = True
                self.color = self.hover_color
                self.call_back('on_enter')

    def _on_leave(self, event, **kwargs):
        if hasattr(event, 'body'):
            if event.body == self:
                self.dirty = 1
                self.mouse_entered = False
                self.color = self.normal_color
                self.call_back('on_leave')

    def _on_pressed(self, event, **kwargs):
        if hasattr(event, 'body'):
            if event.body == self:
                self.dirty = 1
                self.color = self.pressed_color
                self.call_back('on_pressed')

    def _on_release(self, event, **kwargs):
        if hasattr(event, 'body'):
            if event.body == self:
                self.dirty = 1
                self.color = self.released_color
                self.call_back('on_release')

    def set_bold(self, value):
        self.bold = value

    def process_event(self, event):                    
        if event.type in self.listeners:
            self.handle_event(event)
            
        if not self.disabled:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if self.mouse_entered:
                        emit_event(ON_RELEASE, body=self)

    def call_back(self, key):
        if key in self.state_commands:
            cb, args, kwargs = self.state_commands[key]
            return cb(*args, **kwargs)      

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos) and not self.mouse_entered:
            if not self.disabled:           
                emit_event(ON_ENTER, body=self)

        elif not self.rect.collidepoint(mouse_pos) and self.mouse_entered:
            if not self.disabled: 
                emit_event(ON_LEAVE, body=self)
        
        if self.mouse_entered and Input.leftmousedown():
            if not self.disabled: 
                emit_event(ON_PRESSED, body=self)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        if self.text:
            text_display = self.draw_text()
            text_display_rect = text_display.get_rect(center=self.rect.center)
            screen.blit(text_display, text_display_rect)

    def update_image(self, image_name):
        self.image = Content.Image.load(image_name)

    def draw_text(self):
        self.font = Content.Font.get_font('Inconsolata')
        self.font.set_bold(self.bold)
        self.text_display = self.font.render(self.text, True, self.color)
        return self.text_display
